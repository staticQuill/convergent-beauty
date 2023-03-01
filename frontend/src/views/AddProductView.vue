/* eslint-disable  @typescript-eslint/no-explicit-any */

<script setup lang="ts">
import { storeToRefs } from 'pinia';

import { userAuthStore } from '@/stores/auth.store';

import { ref } from "vue";
import router from "@/router";
import {useRoute} from "vue-router";
import {auto} from "@popperjs/core";
import piniaPluginPersistedState from "pinia-plugin-persistedstate";

const authStore = userAuthStore();
const { user: authUser } = storeToRefs(authStore);

let indices = ref([{name: "foundation-concealer"}, {name: "lip color"}]);

let suggestions = ref([])

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
    body: JSON.stringify({refresh: JSON.parse(authStore.user.refreshToken)}),
  };
  console.log(authRequestOptions)
  const tokenJson = await fetch("http://188.166.174.54/auth/login/refresh/", authRequestOptions);
  let tokens = await tokenJson.json()
  authStore.user.bearerToken = "Bearer".concat(" ", tokens.access)
  localStorage.setItem('user', JSON.stringify(authStore.user))
  return true
}

let brandString = ref("");
let productString = ref("");
let listingBrands = false
let listingProducts = false

let typeDefined: string = JSON.stringify(useRoute().query.type) || localStorage.getItem("type") || ""
let brandDefined: string = JSON.stringify(useRoute().query.brand) || localStorage.getItem("brand") || ""
let productDefined: string = JSON.stringify(useRoute().query.product) || localStorage.getItem("product") || ""

localStorage.setItem("type", typeDefined)
localStorage.setItem("brand", brandDefined)
localStorage.setItem("product", productDefined)

console.log(typeDefined)
console.log(brandDefined)
console.log(productDefined)
const mockBrands = [
  {name: "Estee Lauder"},
  {name: "Estimation"},
]

const mockProducts = [
  {name: "Divine Lipcolor"},
  {name: "Matte Lipcolor"},
]

let autocompleteResults = ref([{name: "start typing to see suggestions"}])


async function getBrandSuggestions () {
  if (brandString.value.length >= 3) {
    let retryRequest = false
    do {
      let endpointWithQuery = "http://188.166.174.54/search".concat("?brand=", brandString.value, "&type=", typeDefined)
      let authRequestOptions = {
        method: "GET",
        headers: {"Content-Type": "application/json", "Authorization": authStore.user.bearerToken}
      };
      /* let suggestionJson = await fetch(endpointWithQuery, authRequestOptions);
      if (retryRequest && suggestionJson.status === 401) {
        break
      } else if (suggestionJson.status === 401) {
        retryRequest = await useRefreshToken()
      } else {
        suggestions.value = await suggestionJson.json()
      }*/
    } while (retryRequest);
    listingBrands = true;
    autocompleteResults.value = mockBrands;
  }
}

async function getProductSuggestions () {
  if (productString.value.length >= 3) {
    let retryRequest = false
    do {
      let endpointWithQuery = "http://188.166.174.54/search".concat("?brand=", brandString.value, "&type=", typeDefined)
      let authRequestOptions = {
        method: "GET",
        headers: {"Content-Type": "application/json", "Authorization": authStore.user.bearerToken}
      };
      /* let suggestionJson = await fetch(endpointWithQuery, authRequestOptions);
      if (retryRequest && suggestionJson.status === 401) {
        break
      } else if (suggestionJson.status === 401) {
        retryRequest = await useRefreshToken()
      } else {
        suggestions.value = await suggestionJson.json()
      }*/
    } while (retryRequest);
    autocompleteResults.value = mockProducts;
    listingProducts = true;
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
            <input name="type" type="radio" :value="index.name"/>{{ index.name }}
          </div>

          <button class="btn btn-primary" :disabled="isSubmitting">
            <span v-show="isSubmitting" class="spinner-border spinner-border-sm mr-1"></span>
            choose product type
          </button>
        </form>
      </div>
    </div>

    <div v-if="typeDefined.length > 0 && brandDefined.length === 0">
      <h1>What brand of {{ typeDefined }} do you wish to enter?</h1>
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

          <router-link :to="{ path: '/product-notes', query: {brand: brandDefined, product: productDefined} }">
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
