<script setup>
import { storeToRefs } from 'pinia';

import { userAuthStore } from '@/stores/auth.store';

import { ref } from "vue";

const authStore = userAuthStore();
const { user: authUser } = storeToRefs(authStore);

async function useRefreshToken () {
  console.log("refresh token")
  console.log(authStore.user.refreshToken)
  let authRequestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: {refresh: authStore.user.refreshToken.replace(/['"]+/g, '')},
  };
  console.log(authRequestOptions)
  const tokenJson = await fetch("http://188.166.174.54:8080/auth/login/refresh/", authRequestOptions);
  let tokens = await tokenJson.json()
  authStore.user.bearerToken = "Bearer".concat(" ", tokens.access)
  localStorage.setItem('user', JSON.stringify(authStore.user))
  return true
}

let products = ref("loading...")

let retryRequest = false
let productsJson = {};
do {
  let authRequestOptions = {
    method: "GET",
    headers: { "Content-Type": "application/json", "Authorization": authStore.user.bearerToken }
  };
  productsJson = await fetch("http://188.166.174.54:8080/user-products/", authRequestOptions);
  if (retryRequest) {
    break
  }
  if (productsJson.status === 401) {
    retryRequest = await useRefreshToken()
  }
} while (retryRequest === true);

products.value = await productsJson.json()
</script>

<template>
  <Suspense>
    <div>
      <h1>Hi, {{authUser?.username}}</h1>
      <div class="float-box centered-box">
        <h1>You've entered the following products:</h1>
      </div>
      <div v-for="product in products" class="float-box list-block-item" :key="product">
        <p class="brand-name">{{ product.product.brand.name }}</p>
        <p class="product-type">{{ product.product.type }}</p>
        <p class="product-name">{{ product.product.name }}</p>
        <p>Texture notes: </p>
        <ul>
          <li v-for="texture in product.texture_notes" v-bind:key="scent">
            You felt it was {{texture}}
          </li>
          <li v-for="(rating, texture) in product.product.texture_ratings" v-bind:key="texture">
            {{rating}} user(s) felt it was {{texture}}
          </li>
        </ul>
        <p>You had the following feelings on this product's texture:</p>
        <ul>
          <li v-for="feel in product.texture_enjoyment" v-bind:key="feel">
            You felt it was {{feel}}
          </li>
        </ul>
        <p>Scent notes: </p>
        <ul>
          <li v-for="scent in product.scent_notes" v-bind:key="scent">
            You felt it was {{scent}}
          </li>
          <li v-for="(rating, scent) in product.product.scent_ratings" v-bind:key="scent">
            {{rating}} user(s) felt it was {{scent}}
          </li>
        </ul>
        <p>You had the following feelings on this product's scent:</p>
        <ul>
          <li v-for="feel in product.scent_enjoyment" v-bind:key="feel">
            You felt it was {{feel}}
          </li>
        </ul>
        <p>Overall, these were your feelings on the product:</p>
        <ul>
          <li v-for="feel in product.overall_sentiments" v-bind:key="feel">
            {{feel}}
          </li>
        </ul>
        <p>You left this custom note:</p>
        <p><i>{{ product.custom_notes }}</i></p>
      </div>
    </div>
  </Suspense>
</template>
