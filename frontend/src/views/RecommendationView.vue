<script setup>
import { storeToRefs } from 'pinia';

import { userAuthStore } from '@/stores/auth.store';

import { ref } from "vue";

const authStore = userAuthStore();
const { user: authUser } = storeToRefs(authStore);

let recommendations = ref("loading...")

console.log({ "refresh": JSON.parse(authStore.user.refreshToken)})

let retryRequest = false
let recJson = {};
do {
  let authRequestOptions = {
    method: "GET",
    headers: { "Content-Type": "application/json", "Authorization": authStore.user.bearerToken }
  };
  recJson = await fetch("http://188.166.174.54/recommendations/", authRequestOptions);
  if (retryRequest) {
    break
  }
  if (recJson.status === 401) {
    authRequestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({refresh: JSON.parse(authStore.user.refreshToken)}),
    };
    const tokenJson = await fetch("http://188.166.174.54/auth/login/refresh/", authRequestOptions);
    let tokens = await tokenJson.json()
    authStore.user.bearerToken = "Bearer".concat(" ", tokens.access)
    localStorage.setItem('user', JSON.stringify(authStore.user))
    retryRequest = true
  }
} while (retryRequest === true);

recommendations.value = await recJson.json()
</script>

<template>
  <Suspense>
    <div>
      <h1>Hi, {{authUser?.username}}</h1>
      <div class="float-box centered-box">
        <h1>Your recommendations:</h1>
      </div>
      <div v-for="recommendation in recommendations" class="float-box list-block-item" :key="recommendation">
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
    </div>
  </Suspense>
</template>
