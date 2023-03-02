/* eslint-disable  @typescript-eslint/no-explicit-any */

<script setup lang="ts">
import {storeToRefs} from 'pinia';

import {userAuthStore} from '@/stores/auth.store';

import {ref} from "vue";
import {LocationQueryValue, useRoute} from "vue-router";
import router from "@/router";

const authStore = userAuthStore();
const { user: authUser } = storeToRefs(authStore);

let indices = ref([
  {name: "skincare, like lotion or cleanser", value: "skincare"},
  {name: "lip color or lip balm", value: "lip"},
  {name: "foundation or concealer", value: "foundation-concealer"},
  {name: "blush, bronzer, or other cheek color", value: "cheek"},
  {name: "body scents, like perfume or cologne", value: "perfume-cologne"},
  {name: "eyeshadow", value: "eyeshadow"},
  {name: "eyeliner", value: "eyeliner"},
  {name: "mascara", value: "mascara"},
  {name: "hair products, including shampoo and conditioner", value: "hair"},
  {name: "any other product", value: "other"},
]);

let suggestions = ref({"filtered": [], "raw": []})

interface formObject {
  brand: string,
  type: string
}

async function useRefreshToken () {
  console.log("refresh token")
  console.log(authStore.user.refreshToken)
  let authRequestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({refresh: authStore.user.refreshToken.replace(/['"]+/g, '')}),
  };
  console.log(authRequestOptions)
  const tokenJson = await fetch("http://188.166.174.54:8080/auth/login/refresh/", authRequestOptions);
  let tokens = await tokenJson.json()
  authStore.user.bearerToken = "Bearer".concat(" ", tokens.access)
  localStorage.setItem('user', JSON.stringify(authStore.user))
  return true
}

let brandString = ref("");
let productString = ref("");
let listingBrands = false
let listingProducts = false

function getDefinedString(queryParam: string | LocationQueryValue[] | LocationQueryValue, definer: string) {
  if (queryParam) {
    return queryParam.toString().replace(/['"]+/g, '')
  } else {
    return localStorage.getItem(definer) || ""
  }
}

let typeDefined: string = getDefinedString(useRoute().query.type, "type")
let brandDefined: string = getDefinedString(useRoute().query.brand, "brand")
let productDefined: string = getDefinedString(useRoute().query.product, "product")

localStorage.setItem("type", typeDefined)
localStorage.setItem("brand", brandDefined)
localStorage.setItem("product", productDefined)

console.log(typeDefined)
console.log(brandDefined)
console.log(productDefined)

let autocompleteResults = ref([{name: "start typing to see suggestions"}])


async function getBrandSuggestions () {
  if (brandString.value.length >= 1) {
    let retryRequest = false
    do {
      let endpointWithQuery = "http://188.166.174.54:8080/search/autocomplete".concat("?field=brand&partial=", brandString.value, "&type=", typeDefined)
      let authRequestOptions = {
        method: "GET",
        headers: {"Content-Type": "application/json", "Authorization": authStore.user.bearerToken}
      };
      let suggestionJson = await fetch(endpointWithQuery, authRequestOptions);
      if (retryRequest && suggestionJson.status === 401) {
        break
      } else if (suggestionJson.status === 401) {
        retryRequest = await useRefreshToken()
      } else {
        suggestions.value = await suggestionJson.json()
      }
    } while (retryRequest);
    listingBrands = true;
    autocompleteResults.value = suggestions.value.filtered
  }
}

async function getProductSuggestions () {
  if (productString.value.length >= 1) {
    let retryRequest = false
    do {
      let endpointWithQuery = "http://188.166.174.54:8080/search/autocomplete".concat("?field=product&brand=", brandDefined, "&type=", typeDefined, "&partial=", productString.value)
      let authRequestOptions = {
        method: "GET",
        headers: {"Content-Type": "application/json", "Authorization": authStore.user.bearerToken}
      };
      let suggestionJson = await fetch(endpointWithQuery, authRequestOptions);
      if (retryRequest && suggestionJson.status === 401) {
        break
      } else if (suggestionJson.status === 401) {
        retryRequest = await useRefreshToken()
      } else {
        suggestions.value = await suggestionJson.json()
      }
    } while (retryRequest);
    listingProducts = true;
    autocompleteResults.value = suggestions.value.filtered
  }
}

function setBrand (result: string) {
  brandString.value = result
  listingBrands = false
}

function setProduct (result: string) {
  productString.value = result
  listingProducts = false
}

function resetFields (levels: number) {
  if (levels > 0) {
    let productDefined: string = ""
    localStorage.setItem("product", productDefined)
  }
  if (levels > 1) {
    let brandDefined: string = ""
    localStorage.setItem("brand", brandDefined)
  }
  if (levels > 2) {
    let typeDefined: string = ""
    localStorage.setItem("type", typeDefined)
    let scentsDefined: string = ""
    localStorage.setItem("scentsDefined", scentsDefined)
    let texturesDefined: string = ""
    localStorage.setItem("texturesDefined", texturesDefined)
    let sentimentsDefined: string = ""
    localStorage.setItem("sentimentsDefined", sentimentsDefined)
    router.push("/new-product")
  }
}

let isSubmitting = false

</script>

<template>
    <div v-if="typeDefined.length === 0 && brandDefined.length === 0">
      <h1>What type of product do you want to enter?</h1>
      <div class="float-box list-block-item">
        <form >
          <div v-for="index in indices" :key="index">
            <input name="type" type="radio" :value="index.value"/>{{ index.name }}
          </div>

          <button class="btn btn-primary" :disabled="isSubmitting">
            <span v-show="isSubmitting" class="spinner-border spinner-border-sm mr-1"></span>
            choose product type
          </button>
        </form>
      </div>
    </div>

    <div v-if="typeDefined.length > 0 && brandDefined.length === 0">
      <h1>What brand do you wish to enter?</h1>
      <div class="float-box list-block-item">
        <form >
          <label>Start typing the brand name:</label>
          <input name="brand" type="text" v-model="brandString" v-on:input="getBrandSuggestions" autocomplete="true" />
          <ul v-if="listingBrands">
            <li v-for="result in autocompleteResults" :key="result.name" v-on:click="setBrand(result.name)">
              {{ result.name }}
            </li>
          </ul>

          <button @click="(brandDefined = brandString)" class="btn btn-primary" :disabled="isSubmitting">
            <span v-show="isSubmitting" class="spinner-border spinner-border-sm mr-1"></span>
            choose brand
          </button>

        </form>
        <form >
          <button @click="resetFields(3)" class="btn btn-primary" :disabled="isSubmitting">
            <span v-show="isSubmitting" class="spinner-border spinner-border-sm mr-1"></span>
            go back
          </button>
          <button @click="resetFields(10)" class="btn btn-primary" :disabled="isSubmitting">
            <span v-show="isSubmitting" class="spinner-border spinner-border-sm mr-1"></span>
            start over
          </button>
        </form>
      </div>
    </div>

    <div v-if="brandDefined.length > 0">
      <h1>What product from {{ brandDefined }} do you wish to enter?</h1>
      <div class="float-box list-block-item">
        <form>
          <label>Start typing the product name:</label>
          <input name="product" type="text" v-model="productString" v-on:input="getProductSuggestions" autocomplete="true" />
          <ul v-if="listingProducts">
            <li v-for="result in autocompleteResults" :key="result.name" v-on:click="setProduct(result.name)">
              {{ result.name }}
            </li>
          </ul>

          <router-link :to="{ path: '/product-notes', query: {brand: brandDefined, product: productString} }">
            <span v-show="isSubmitting" class="spinner-border spinner-border-sm mr-1"></span>
            choose product
          </router-link>
        </form>

        <form >
          <button @click="resetFields(2)" class="btn btn-primary" :disabled="isSubmitting">
            <span v-show="isSubmitting" class="spinner-border spinner-border-sm mr-1"></span>
            go back
          </button>
          <button @click="resetFields(10)" class="btn btn-primary" :disabled="isSubmitting">
            <span v-show="isSubmitting" class="spinner-border spinner-border-sm mr-1"></span>
            start over
          </button>
        </form>
      </div>
    </div>


</template>
