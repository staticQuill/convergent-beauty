<script setup lang="ts">

import { storeToRefs } from 'pinia';

import { userAuthStore } from '@/stores/auth.store';

import { ref } from "vue";
import type {LocationQueryValue} from "vue-router";
import {useRoute} from "vue-router";
import router from "@/router";

const authStore = userAuthStore();
const { user: authUser } = storeToRefs(authStore);

async function useRefreshToken () {
  console.log("refresh token")
  console.log(authStore.user.refreshToken)
  let authRequestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({refresh: JSON.parse(authStore.user.refreshToken)}),
  };
  console.log(authRequestOptions)
  const tokenJson = await fetch("https://188.166.174.54:8080/auth/login/refresh/", authRequestOptions);
  let tokens = await tokenJson.json()
  authStore.user.bearerToken = "Bearer".concat(" ", tokens.access)
  localStorage.setItem('user', JSON.stringify(authStore.user))
  return true
}

let responseJson = ref("")

async function postProductSubmit () {
  let retryRequest = false
  let productJson = JSON.stringify({
    brand_name: brandDefined,
    product_name: productDefined,
    type: typeDefined,
    texture_notes: textureList ,
    scent_notes: scentList,
    texture_enjoyment: textureFeelList,
    scent_enjoyment: scentFeelList,
    sentiments: generalFeelList,
    custom_notes: generalNotes
  })
  console.log(productJson)
  do {
    let endpoint = "https://188.166.174.54:8080/user-products/"
    let authRequestOptions = {
      method: "POST",
      headers: {"Content-Type": "application/json", "Authorization": authStore.user.bearerToken},
      body: productJson
    };
    let response = await fetch(endpoint, authRequestOptions);
    if (retryRequest && response.status === 401) {
      break
    } else if (response.status === 401) {
      retryRequest = await useRefreshToken()
    } else {
      responseJson.value = JSON.stringify(await response.json())
      retryRequest = false
    }
  } while (retryRequest);
  console.log(JSON.stringify(responseJson.value))
  localStorage.setItem("responseJson",  JSON.stringify(responseJson.value))
  resetFields(10)
}


const textures = [
  {name: "sticky", value: "sticky"},
  {name: "smooth", value: "smooth"},
  {name: "slimy", value: "slimy"},
  {name: "cakey or thick", value: "cakey"},
  {name: "rough or gritty", value: "rough"},
  {name: "wet", value: "wet"},
  {name: "creamy", value: "creamy"},
  {name: "greasy or oily", value: "greasy"},
  {name: "not applicable/none of the above", value: "na"}
]


const scents = [
  {name: "fruity", value: "fruity"},
  {name: "clean or antiseptic", value: "clean"},
  {name: "floral", value: "floral;"},
  {name: "sweet or sugary", value: "sweet"},
  {name: "not applicable/none of the above", value: "na"}
]

const scentSentiments = [
  {"text": "I liked the scent", "value": "pleasant"},
  {"text": "I disliked the scent", "value": "unpleasant"},
  {"text": "I was neutral on the scent", "value": "neutral"},
  {"text": "I found the scent overpowering", "value": "overpowering"}
]

const textureSentiments = [
  {"text": "I liked the texture", "value": "pleasant"},
  {"text": "I disliked the texture", "value": "unpleasant"},
  {"text": "I was neutral on the texture", "value": "neutral"},
  {"text": "I found the texture overpowering", "value": "overpowering"}
]

const generalSentiments = [
  {"text": "I liked this product overall", "value": "liked"},
  {"text": "I disliked the product overall", "value": "disliked"},
  {"text": "I was neutral on this product overall", "value": "neutral"},
  {"text": "I thought it looked good on me", "value": "looks good"},
  {"text": "I thought it looked wrong on me", "value": "looks wrong"}
]


function resetFields (levels: number) {
  if (levels > 1) {
    let scentsDefined: string = ""
    localStorage.setItem("scentsDefined", scentsDefined)
  }
  if (levels > 2) {
    let texturesDefined: string = ""
    localStorage.setItem("texturesDefined", texturesDefined)
  }
  if (levels > 3) {
    let productDefined: string = ""
    localStorage.setItem("product", productDefined)
    let brandDefined: string = ""
    localStorage.setItem("brand", brandDefined)
    let typeDefined: string = ""
    localStorage.setItem("type", typeDefined)
  }
  if (levels > 0) {
    let defaultSentiment: string = ""
    localStorage.setItem("scentSentiment", defaultSentiment)
    localStorage.setItem("textureSentiment", defaultSentiment)
    localStorage.setItem("generalSentiment", defaultSentiment)
    localStorage.setItem("generalNotes", defaultSentiment)
    router.push("/new-product")
  }
}

function getDefinedString(queryParam: string | LocationQueryValue[] | LocationQueryValue, definer: string) {
  if (queryParam) {
    return queryParam.toString().replace(/["]+/g, '')
  } else {
    return localStorage.getItem(definer) || ""
  }
}

let texturesDefined: string = getDefinedString(useRoute().query.texturesDefined, "texturesDefined")

localStorage.setItem("texturesDefined", texturesDefined)

let scentsDefined: string = getDefinedString(useRoute().query.scentsDefined, "scentsDefined")

localStorage.setItem("scentsDefined", scentsDefined)

let typeDefined: string = getDefinedString(useRoute().query.type, "type")
let brandDefined: string = getDefinedString(useRoute().query.brand, "brand")
let productDefined: string = getDefinedString(useRoute().query.product, "product")

localStorage.setItem("type", typeDefined)
localStorage.setItem("brand", brandDefined)
localStorage.setItem("product", productDefined)

let textureSentiment= ref(getDefinedString(useRoute().query.textureFeels, "textureSentiment"))
let scentSentiment= ref(getDefinedString(useRoute().query.scentFeels, "scentSentiment"))
let generalSentiment = ref(getDefinedString(useRoute().query.generalFeels, "generalSentiment"))
let generalNotes: string = getDefinedString(useRoute().query.generalNotes, "generalNotes")

localStorage.setItem("textureSentiment", textureSentiment.value)
localStorage.setItem("scentSentiment", scentSentiment.value)
localStorage.setItem("generalSentiment", generalSentiment.value)
localStorage.setItem("generalNotes", generalNotes)

let loggingProduct = ref(false)
let isSubmitting = false

let textureList = texturesDefined.split(",")
if (textureList.includes("na")) {
  textureList.splice(textureList.indexOf("na"), 1)
}
let scentList = scentsDefined.split(",")
if (scentList.includes("na")) {
  scentList.splice(scentList.indexOf("na"), 1)
}
let textureFeelList = textureSentiment.value.split(",")
let scentFeelList = scentSentiment.value.split(",")
let generalFeelList = generalSentiment.value.split(",")

</script>

<template>
    <div>
      <div v-if="!texturesDefined">
        <h1>How would you describe the <b>texture</b> of the {{productDefined}} by {{brandDefined}}? Pick at least one or "not applicable".</h1>
          <div class="float-box list-block-item">
          <form >
            <div v-for="texture in textures" class="input-list" :key="texture.value">
              <input name="texturesDefined" type="checkbox" :value="texture.value"/>{{ texture.name }}
            </div>

            <button class="btn btn-primary dropdown-submit" :disabled="isSubmitting">
              <span v-show="isSubmitting" class="spinner-border spinner-border-sm mr-1"></span>
              set texture notes
            </button>
          </form>
            <br>
            <br>
            <form class="back-buttons">
              <button type="button" @click="resetFields(2)" class="btn btn-primary" :disabled="isSubmitting">
                <span v-show="isSubmitting" class="spinner-border spinner-border-sm mr-1"></span>
                go back
              </button>
              <button type="button" @click="resetFields(10)" class="btn btn-primary" :disabled="isSubmitting">
                <span v-show="isSubmitting" class="spinner-border spinner-border-sm mr-1"></span>
                start over
              </button>
            </form>
        </div>
      </div>

      <div v-if="texturesDefined && !scentsDefined">
        <h1>How would you describe the <b>scent</b> of the {{productDefined}} by {{brandDefined}}? Pick at least one or "not applicable".</h1>
        <div class="float-box list-block-item">
          <form >
            <div v-for="scent in scents" class="input-list" :key="scent.value">
              <input name="scentsDefined" type="checkbox" :value="scent.value"/>{{ scent.name }}
            </div>
            <button class="btn btn-primary" :disabled="isSubmitting">
              <span v-show="isSubmitting" class="spinner-border spinner-border-sm mr-1"></span>
              set scent notes
            </button>
          </form>
          <br>
          <br>
          <form class="back-buttons">
            <button type="button" @click="resetFields(2)" class="btn btn-primary" :disabled="isSubmitting">
              <span v-show="isSubmitting" class="spinner-border spinner-border-sm mr-1"></span>
              go back
            </button>
            <button type="button" @click="resetFields(10)" class="btn btn-primary" :disabled="isSubmitting">
              <span v-show="isSubmitting" class="spinner-border spinner-border-sm mr-1"></span>
              start over
            </button>
          </form>
        </div>
      </div>

      <div v-if="scentsDefined && texturesDefined && !loggingProduct && !(scentSentiment || textureSentiment || generalSentiment)">
        <h1>How did you feel about {{productDefined}} by {{brandDefined}}?</h1>
        <div class="float-box list-block-item">
          <form >
            <br>
            <p>Scent:</p>
            <div v-for="sentiment in scentSentiments" class="input-list" :key="sentiment.value">
              <input name="scentFeels" type="checkbox" :value="sentiment.value" />{{ sentiment.text }}
            </div>
            <br>
            <p>Texture:</p>
            <div v-for="sentiment in textureSentiments" class="input-list" :key="sentiment.value">
              <input name="textureFeels" type="checkbox" :value="sentiment.value" />{{ sentiment.text }}
            </div>
            <br>
            <p>Overall:</p>
            <div v-for="sentiment in generalSentiments" class="input-list" :key="sentiment.value">
              <input name="generalFeels" type="checkbox" :value="sentiment.value" />{{ sentiment.text }}
            </div>
            <br>
            <p>Add any more notes on this project (these are only for you and kept private):</p>
            <textarea name="generalNotes" v-model="generalNotes"/>
            <br>
            <button class="btn btn-primary" :disabled="isSubmitting">
              <span v-show="isSubmitting" class="spinner-border spinner-border-sm mr-1"></span>
              log your feelings
            </button>
          </form>
          <br>
          <br>
          <form class="back-buttons">
            <button type="button" @click="resetFields(2)" class="btn btn-primary" :disabled="isSubmitting">
              <span v-show="isSubmitting" class="spinner-border spinner-border-sm mr-1"></span>
              go back
            </button>
            <button type="button" @click="resetFields(10)" class="btn btn-primary" :disabled="isSubmitting">
              <span v-show="isSubmitting" class="spinner-border spinner-border-sm mr-1"></span>
              start over
            </button>
          </form>
        </div>
      </div>

      <div v-if="(scentSentiment || textureSentiment || generalSentiment) && !responseJson">
        <h1>Please review your submission:</h1>
        <div class="float-box list-block-item">
          <br>
          <p>You submitted the product "{{ productDefined }}" from {{ brandDefined }}</p>
          <p>You found its texture:</p>
          <ul>
            <li v-for="texture in textureList" :key="texture">{{ texture }}</li>
            <li v-for="feeling in textureFeelList" :key="feeling">{{ feeling }}</li>
          </ul>
          <p>You found its scent:</p>
          <ul>
            <li v-for="scent in scentList" :key="scent">{{ scent }}</li>
            <li v-for="feeling in scentFeelList" :key="feeling">{{ feeling }}</li>
          </ul>
          <p>Overall, your thoughts on the product:</p>
          <ul>
            <li v-for="feeling in generalFeelList" :key="feeling">{{ feeling }}</li>
          </ul>
          <p>you left the following custom notes:</p>
          <p><i>{{ generalNotes || "none" }}</i></p>

          <button @click="postProductSubmit" class="btn btn-primary" :disabled="isSubmitting">
            <span v-show="isSubmitting" class="spinner-border spinner-border-sm mr-1"></span>
            submit this product
          </button>
          <br>
          <br>
          <form  class="back-buttons">
            <button type="button" @click="resetFields(2)" class="btn btn-primary" :disabled="isSubmitting">
              <span v-show="isSubmitting" class="spinner-border spinner-border-sm mr-1"></span>
              go back
            </button>
            <button type="button" @click="resetFields(10)" class="btn btn-primary" :disabled="isSubmitting">
              <span v-show="isSubmitting" class="spinner-border spinner-border-sm mr-1"></span>
              start over
            </button>
          </form>
        </div>
      </div>

      <div v-if="responseJson">
        <p>{{ responseJson }}</p>
      </div>
    </div>
</template>
