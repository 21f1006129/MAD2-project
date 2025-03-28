<script setup>
      import { RouterLink } from 'vue-router';

</script>
<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">HHS Admin</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item">
          <router-link class="nav-link" to="/admin">Home</router-link>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            Service
          </a>
          <ul class="dropdown-menu">
            <li>
              <router-link class="dropdown-item" to="/admin/service/view">
                View
              </router-link>
            </li>
            <li>
              <router-link class="dropdown-item" to="/admin/service">
                Create
              </router-link>
            </li>
          </ul>
        </li>

        <li class="nav-item">
          <router-link class="nav-link" to="/admin/service_professionals">Service Professionals</router-link>
        </li>

        <li class="nav-item">
          <router-link class="nav-link" to="/admin/customers">Customers</router-link>
        </li>

        <li class="nav-item">
                <p class="nav-link" href="#" @click="export_file()">Export</p>
        </li>

        <li class="nav-item">
          <router-link class="nav-link" to="/signout">sign out</router-link>
        </li>
      </ul>
    </div>
  </div>
</nav>
</template>

<script>
  export default {
    data(){
      return {
        export_id: null,
      }
    },
    methods:{
      export_file(){
        fetch(import.meta.env.VITE_BASEURL+"/export").then(x =>{
          return x.json()
        }).then(x =>{
          this.export_id = x["id"]
          setTimeout(()=> this.export_status(this.export_id), 2000)
        })
      },
      export_status(id){
        fetch(import.meta.env.VITE_BASEURL+"/export/"+id+"/status").then(x =>{
          return x.json()
        }).then(x =>{
        
          if(x["status"] == "SUCCESS"){
            open(import.meta.env.VITE_BASEURL+`/export/${id}`)
          }
          else{
            setTimeout(()=> this.export_status(this.export_id), 2000)
          }

        })
      }
    }
  }
</script>