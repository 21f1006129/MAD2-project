<script setup>
    import store from '@/store';
</script>
<template>
    <div>
      <div class="d-flex justify-content-center my-3">
      <input type="text" v-model="searchQuery" class="form-control mb-3" placeholder="Search by name" style="max-width: 300px"/>
    </div>
    <table class="table">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Name</th>
          <th scope="col">Username</th>
          <th scope="col">Account Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(customer,index) in filteredCustomers" :key="index">
          <th scope="row">{{ index+1 }}</th>
          <td>{{customer['name']}}</td>
          <td>{{customer['username']}}</td>
          <td>{{ customer['active'] === false ? 'Not Active' : 'Active' }}</td>
          <td>
            <button :class="customer['active'] === false ? 'btn btn-success' : 'btn btn-danger'"
            @click="status_change(customer['id'])">
                {{ customer['active'] === false ? 'Activate' : 'Deactivate' }}
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
                store.dispatch("getCustomers")
            },
            data() {
                return {
                    searchQuery: "",  
                } 
            },
            computed: {
              filteredCustomers() {
                return this.$store.getters.getCustomers.filter(customer => 
                  customer.name.toLowerCase().includes(this.searchQuery.toLowerCase())
                );
              }
            },
            methods:{
                status_change(id){
                  fetch(import.meta.env.VITE_BASEURL+`/customers/status/${id}`,{
                    method: 'PATCH',
                    headers: {
                        "Authentication-Token": store.getters.getToken,
                        "Content-Type": "application/json"
                    }
                }).then(x =>{
                    if(x.status == 200){
                        store.dispatch("getCustomers");
                    }
                })
                }
            }   
        }
    </script>
    
    <style scoped>
    
    </style>