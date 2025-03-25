<script setup>
    import { RouterView } from "vue-router"
    import ServiceProfessionalNavbar from "@/components/serviceprofessional/Navbar.vue"
</script>
<template>
    <div>
        <ServiceProfessionalNavbar/>
        <RouterView/>
        
    </div>

</template>