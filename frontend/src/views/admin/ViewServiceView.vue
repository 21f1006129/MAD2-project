<script setup>
    import store from '@/store';
    import router from '@/router';
</script>
<template>
  <table class="table">
    <thead>
      <tr>
        <th scope="col">#</th>
        <th scope="col">Name</th>
        <th scope="col">Price</th>
        <th scope="col">Description</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(service,index) in store.getters.getServices" :key="index">
        <th scope="row">{{ index+1 }}</th>
        <td>{{service['name']}}</td>
        <td>{{service['price']}}</td>
        <td>{{ service['description'] }}</td>
        <td>
          <button class="btn btn-primary" @click="redirect( service['id'] )">
            Edit
          </button>
        </td>

        <td>
          <button class="btn btn-danger" @click="delete_service( service['id'] )">
            Delete
          </button>
        </td>
      </tr> 

    </tbody>
  </table>
</template>

<script>

    export default {
        created(){
            store.dispatch("getServices")
        },
        methods:{
            redirect(id){
              router.push(`/admin/service/${id}`)
            },
            delete_service(id){
              fetch(import.meta.env.VITE_BASEURL+`/service/delete/${id}`,{
                method: 'DELETE',
                headers: {
                    "Authentication-Token": store.getters.getToken
                }
            }).then(x =>{
                if(x.status == 200){
                    store.dispatch("getServices");

                }
            })
            }
        }   
    }
</script>

<style scoped>

</style>
