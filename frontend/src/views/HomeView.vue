<script setup>
import { storeToRefs } from 'pinia';

import { userAuthStore } from '@/stores/auth.store';

import { ref } from "vue";

const authStore = userAuthStore();
const { user: authUser } = storeToRefs(authStore);

let recommendations = ref("loading...")

console.log(authStore.user.bearerToken)

</script>

<template>
  <Suspense>
    <div>
      <h1>Hi, {{authUser?.username}}</h1>
      <RouterLink to="/new-product">
      <div aria-label="Add a product" class="float-box centered-box">
        <p>Add a product</p>
      </div>
      </RouterLink>
      <RouterLink to="/recommendations">
      <div class="float-box centered-box">
        <p>Go to your recommendations</p>
      </div>
      </RouterLink>
      <RouterLink to="/your-products">
      <div class="float-box centered-box">
        <p>View products you own</p>
      </div>
      </RouterLink>
      <div class="float-box centered-box">
        <p>Adjust your sensory profile (COMING SOON)</p>
      </div>
    </div>
  </Suspense>
</template>
