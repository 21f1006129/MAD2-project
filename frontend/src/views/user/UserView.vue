<script setup>
    import { RouterView } from "vue-router"
    import UserNavbar from "@/components/user/Navbar.vue"
</script>
<template>
    <div>
        <UserNavbar/>
        <RouterView/>
        
    </div>

</template>