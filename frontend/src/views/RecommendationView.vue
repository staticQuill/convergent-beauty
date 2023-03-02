<script setup>
import { storeToRefs } from 'pinia';

import { userAuthStore } from '@/stores/auth.store';

import { ref } from "vue";
import router from "@/router";

const authStore = userAuthStore();
const { user: authUser } = storeToRefs(authStore);

let recommendations = ref({"error": "", "recommendations": []})

async function useRefreshToken () {
  console.log("refresh token")
  console.log(authStore.user.refreshToken)
  let authRequestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({refresh: authStore.user.refreshToken}),
  };
  console.log(authRequestOptions)
  const tokenJson = await fetch("http://188.166.174.54:8080/auth/login/refresh/", authRequestOptions);
  let tokens = await tokenJson.json()
  authStore.user.bearerToken = "Bearer".concat(" ", tokens.access)
  localStorage.setItem('user', JSON.stringify(authStore.user))
  return true
}

async function generateProfile () {
  let retryRequest = false
  let recJson = {};
  do {
    let authRequestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json", "Authorization": authStore.user.bearerToken }
    };
    recJson = await fetch("http://188.166.174.54:8080/preferences/", authRequestOptions);
    if (retryRequest) {
      break
    }
    console.log(recJson.status)
    if (recJson.status === 404) {
      recommendations.value.error = "you must add your own products before you can generate recommendations!"
    } else if (recJson.status === 401) {
      retryRequest = await useRefreshToken()
    } else {
      router.go(0)
    }
  } while (retryRequest === true);
}

let retryRequest = false
let recJson = {};
do {
  let authRequestOptions = {
    method: "GET",
    headers: { "Content-Type": "application/json", "Authorization": authStore.user.bearerToken }
  };
  recJson = await fetch("http://188.166.174.54:8080/recommendations/", authRequestOptions);
  if (retryRequest) {
    break
  }
  console.log(recJson.status)
  if (recJson.status === 404) {
    recommendations.value.error = "you must add your own products before you can generate recommendations!"
  } else if (recJson.status === 401) {
    retryRequest = await useRefreshToken()
  } else {
    recommendations.value = {"error": "", "recommendations": await recJson.json()}
  }
} while (retryRequest === true);

console.log(recommendations.value.error)

</script>

<template>
    <div>
      <h1>Hi, {{authUser?.username}}</h1>
      <div class="float-box centered-box">
        <h1>Your recommendations:</h1>
      </div>
      <div v-if="recommendations.error" class="float-box">
          <p>an error occurred: {{ recommendations.error }}</p>
      </div>
      <div>
        <button class="btn btn-primary" @click="generateProfile">generate your recommendations</button>
      </div>
      </div>
      <div v-for="recommendation in recommendations.recommendations" class="float-box list-block-item" :key="recommendation">
        <p class="brand-name">{{ recommendation.brand.name }}</p>
        <p class="product-type">{{ recommendation.type }}</p>
        <p class="product-name">{{ recommendation.name }}</p>
        <p>Texture notes: </p>
        <ul>
          <li v-for="(rating, texture) in recommendation.texture_ratings" v-bind:key="texture">
            {{rating}} user(s) felt it was {{texture}}
          </li>
        </ul>
        <p>Scent notes: </p>
        <ul>
          <li v-for="(rating, scent) in recommendation.scent_ratings" v-bind:key="scent">
            {{rating}} user(s) felt it was {{scent}}
          </li>
        </ul>
      </div>
</template>
