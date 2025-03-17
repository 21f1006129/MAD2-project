<script setup>
    import { RouterView } from "vue-router"
    import AdminNavbar from "@/components/admin/Navbar.vue"
</script>
<template>
    <div>
        <AdminNavbar/>
        <RouterView/>
    </div>

</template>