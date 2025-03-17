<script setup>
import store from "@/store";
import router from "@/router";
</script>
<template>
    <div>
    <div class="card" >
        <h6 style="color:crimson;text-align: center">{{ error_message }}</h6>
        <div class="card-body">
            <h5 class="card-title">Create New Service</h5>
            <form @submit.prevent="submit()">
                <div class="row">
                    <div class="col">
                    <input type="text" class="form-control" v-model = "servicename" placeholder="Servicename" aria-label="Servicename" required>
                    </div>
                </div>
                <div class="row">
                    <div class="col">
                    <input type="text" class="form-control" v-model="description" placeholder="Description" aria-label="Description" required>
                    </div>
                </div>
                <div class="row">
                    <div class="col">
                    <input type="number" min="100" max="10000" class="form-control" v-model="baseprice" placeholder="baseprice" aria-label="baseprice" >
                    </div>
                </div>
                <div class="row">
                    <div class="col">
                    <input type="submit" class="btn btn-primary" value="Create">
                    </div>
                </div>
            </form>
        </div>
    </div>

    <div class="card" v-if="id">
        <div class="card-body">
            <h5 class="card-title">Edit Service</h5>
            <form @submit.prevent="update()">
                <div class="row">
                    <div class="col">
                    <input type="text" class="form-control" v-model = "editservicename" placeholder="Servicename" aria-label="Servicename" required>
                    </div>
                </div>
                <div class="row">
                    <div class="col">
                    <input type="text" class="form-control" v-model="editdescription" placeholder="Description" aria-label="Description" required>
                    </div>
                </div>
                <div class="row">
                    <div class="col">
                    <input type="number" min="100" max="10000" class="form-control" v-model="editbaseprice" placeholder="baseprice" aria-label="baseprice" >
                    </div>
                </div>
                <div class="row">
                    <div class="col">
                    <input type="submit" class="btn btn-primary" value="Update">
                    </div>
                </div>
            </form>
        </div>
    </div>

</div>
</template>

<script>
export default {
    props: ['id'],
    data(){
        return{
            error_message: null,
            servicename: null,
            description: null,
            baseprice: null,
            editservicename: 'default',
            editdescription:null,
            editbaseprice:null,
            error:{
                mesasge:null
            }
        }

    },
    watch: {
        service(value){
            this.editservicename = value['name'];
            this.editbaseprice = value['price'];
            this.editdescription = value['description'] 
        }

    },
    created(){
        store.dispatch("getServices");
    },
    computed: {
  service() {
     const services = this.$store.getters.getService; 
     for (let i = 0; i < services.length; i++) {
       if (services[i]['id'] === parseInt(this.id)) { 
         return services[i];
       }
     }
     return null; 
  }
},
    methods:{
        validate(){ 
            console.log(this.servicename)

        },
        submit(){
            this.validate()
            fetch(import.meta.env.VITE_BASEURL+"/service/create",{
                method: 'POST',
                headers: {
                    "Content-Type":"application/json",
                    "Authentication-Token": store.getters.getToken
                },
                body: JSON.stringify({servicename: this.servicename, description:this.description, baseprice:this.baseprice})
            }).then(x =>{
                if(x.status == 200){
                    router.push("/admin/service/view")
                }
                else if(x.status == 409){
                    this.error_message = "This Service name already exists";


                }
            })
        },
        update(){
            fetch(import.meta.env.VITE_BASEURL+"/service/update",{
                method: 'POST',
                headers: {
                    "Content-Type":"application/json",
                    "Authentication-Token": store.getters.getToken
                },
                body: JSON.stringify({id:this.id,new_servicename: this.editservicename, new_description:this.editdescription, new_baseprice:this.editbaseprice})
            }).then(x =>{
                if(x.status == 200){
                    router.push("/admin/service/view")
                }
            })

        }
    }
}
</script>

<style scoped>
    .col {
        padding: 5px;
    }
    .card{
        margin: 10px;
    }   
</style>