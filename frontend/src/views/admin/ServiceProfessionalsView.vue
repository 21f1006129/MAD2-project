<script setup>
    import store from '@/store';
</script>
<template>
  <div>
    <div class="d-flex justify-content-center my-3">
      <input type="text" v-model="searchQuery" class="form-control mb-3" placeholder="Search by name..." style="max-width: 300px"/>
    </div>
    <table class="table">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Name</th>
          <th scope="col">Service Type</th>
          <th scope="col">Cumulative Rating</th>
          <th scope="col">Account Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(service_professional,index) in filteredProfessionals" :key="index">
          <th scope="row">{{ index+1 }}</th>
          <td>{{service_professional['name']}}</td>
          <td>{{service_professional['service_type']}}</td>
          <td>{{ Number(service_professional['cumulative_rating']).toFixed(2) }}</td>
          <td>{{ service_professional['active'] === false ? 'Not Active' : 'Active' }}</td>
          <td>
            <button :class="service_professional['active'] === false ? 'btn btn-success' : 'btn btn-danger'"
            @click="status_change(service_professional['id'])">
                {{ service_professional['active'] === false ? 'Activate' : 'Deactivate' }}
                </button>

          </td>
    
        </tr> 
    
      </tbody>
    </table>
  </div>
    </template>
    
    <script>
    
        export default {
            created(){
                store.dispatch("getServiceProfessionals")
            },
            data() {
                return {
                    searchQuery: "",  // Stores user input for searching
                } 
            },
            computed: {
              filteredProfessionals() {
                return this.$store.getters.getServiceProfessionals.filter(service_professional => 
                  service_professional.name.toLowerCase().includes(this.searchQuery.toLowerCase())
                );
              }
            },
            methods:{
                status_change(id){
                  fetch(import.meta.env.VITE_BASEURL+`/service_professionals/status/${id}`,{
                    method: 'PATCH',
                    headers: {
                        "Authentication-Token": store.getters.getToken,
                        "Content-Type": "application/json"
                    }
                }).then(x =>{
                    if(x.status == 200){
                        store.dispatch("getServiceProfessionals");
    
                    }
                })
                }
            }   
        }
    </script>
    
    <style scoped>
    
    </style>