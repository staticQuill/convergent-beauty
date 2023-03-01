<script setup>
import { storeToRefs } from 'pinia';

import { userAuthStore } from '@/stores/auth.store';

import { ref } from "vue";

const authStore = userAuthStore();
const { user: authUser } = storeToRefs(authStore);

</script>

<template>
  <Suspense>
    <div>
      hi
    </div>
  </Suspense>
</template>
