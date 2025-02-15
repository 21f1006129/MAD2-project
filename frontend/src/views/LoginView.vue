<script setup >
import Navbar from '../components/Navbar.vue' 
import store from '../store'
</script>

<template>
    <div>
        <Navbar/>
    <div class="container-fluid"> 
 
        <div class="card" style="width: fit-content;">
             <div class="card-body">
                <h4 class="'card-title'">Login</h4>
                <form @submit.prevent="login()">
                <div class="row">
                    <div class="col">
                    <input type="text" class="form-control" v-model="username" placeholder="username" aria-label="username" required>
                    </div>
                </div>
                <div class="row">
                    <div class="col">
                    <input type="password" class="form-control" v-model="password" placeholder="password" aria-label="password" required>
                    </div>
                </div>
                <div class="row">
                    <div class="col">
                    <input type="submit" class="btn btn-primary" style="width: 100%;" value="Login">
                    </div>
                </div>
                <div class="row">
                    <div class="col" style="display: flex;justify-content: center;">
                           <router-link to="/signup">Register</router-link>
                    </div>
                </div>
                </form>
            </div>
        </div>
        
    </div>

    </div>

</template>
<script>
    export default {
        data(){
            return {
                username : null,
                password : null,
                error : {
                    username : null,
                    password : null
                }
            }
        },
        methods:{
            validate(){
                console.log(this.username, this.password);
            },
            login(){
                this.validate();
            fetch(import.meta.env.VITE_BASEURL+'/signin', {method:"POST",
            headers: {"Content-Type":"application/json"},
            body : JSON.stringify({username: this.username, password: this.password})
            }).then(resp => {
                return [resp.json(),resp.status]
            }).then(x => {
                if(x[1] == 200){
                    return x[0]
                }
                else if (x[1] == 404 || x[1]==400){
                    this.error = {
                        username: "Invalid username or password",
                        password: "Invalid username or password"
                    }
                }
                return {}
            }).then(x=> {
                store.commit("setUser",x);

            })
            }
        }
     }
</script>

<style scoped>
     .container-fluid{
        width:100%;
        height:100vh;
        overflow: hidden;
        display:flex;
        justify-content: center;
        align-items: center;
     }
     .row{
        padding: 10px;
     }
</style>