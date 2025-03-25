<script setup>
import { RouterView } from 'vue-router'
import store from "@/store"

</script>

<template>
      <RouterView/>
</template>
<script>

export default {
  created(){
    let user = localStorage.getItem("user");
    store.commit("setUser", (user) ? JSON.parse(user) : {token: null, roles: []});
    //console.log(store.state.user,"Banzai");
  }
}
</script>

<style scoped>

</style>
