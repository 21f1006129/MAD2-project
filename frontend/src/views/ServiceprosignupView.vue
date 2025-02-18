<script setup >
import Navbar from '../components/Navbar.vue' 
import store from '../store'
import router from '../router/index.js'
</script>

<template>
    <div>
        <Navbar/>
    <div class="container-fluid"> 
 
        <div class="card" style="width: fit-content;">
             <div class="card-body">
              
                <p style="color:green;">{{ message }}</p>
                <p style = 'color:red'>{{ message1 }}</p>
                <h4 class="'card-title'" style="text-align:center">Service Professional Register</h4>
                <form @submit.prevent="signup()">
                <div class="row">
                    <div class="col">
                    <input type="text" class="form-control" v-model="fullname" placeholder="fullname" aria-label="fullname" required>
                    </div>
                </div>
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
                    <input type="password" class="form-control" v-model="confirm_password" placeholder="confirm password" aria-label="confirm password" required>
                    </div>
                </div>
                <p style="color:red;">{{toggle}}</p>
                <div class="row">
                    <div class="col">
                    <input type="number" class="form-control" v-model="pincode" placeholder="Enter 6 digit pincode" aria-label="pincode" required>
                    </div>
                </div>
                <p style="color: red;">{{ pincheck }}</p>
                <div class="row">
                    <p>Select Service Type</p>
                    <select class="form-select form-select-sm" v-model ="service_type" aria-label="Small select example">
                        <option value="1">plumber</option>
                        <option value="2">electrician</option>
                        <option value="3">AC repair</option>
                    </select>

                </div>
                
                <div class="row">
                    <div class="col">
                    <input type="submit" class="btn btn-primary" style="width: 100%;" value="submit">
                    </div>
                </div>
                <div class="row">
                    <div class="col" style="display: flex;justify-content: center;">
                           <router-link to="/">Login</router-link>
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
                fullname: null,
                username : null,
                password : null,
                confirm_password : null,
                service_type : null,
                pincode : null,
                error : {
                    username : null,
                    password : null
                },
                message : null,
                message1 : null
                
            }
        },
        methods:{
            validate(){
                console.log(this.username, this.password);
            },
            signup(){
                this.validate();
                fetch(import.meta.env.VITE_BASEURL+'/servicepro-signup',{method:'POST',headers: {"Content-Type":"application/json"},
                body : JSON.stringify({fullname : this.fullname ,username: this.username, password: this.password, })

                }).then(resp=>{


                    return [resp.json(),resp.status]
                }).then(x=>{
                    console.log('resp 2',x[1]);
                    if (x[1]==200){
                        this.message1 = null;
                        this.message = 'Signup successful! please Login.';
                        this.fullname = null;
                        this.username = null;
                        this.password = null;
                        this.confirm_password = null;
                        router.push({path:"/signup"})
                    }
                    else{
                        this.message = null;
                        this.message1 = 'Username already exists';
                        this.fullname = null;
                        this.username = null;
                        this.password = null;
                        this.confirm_password = null;
                        router.push({path:"/signup"})
                    }
                })
                
                }  
        },
        computed:{
            toggle(){
                if(this.password == this.confirm_password || this.password == '' || this.confirm_password == ''){
                    return ''
                }
                return "Passwords don't match."
            },
            pincheck(){
                return typeof this.pincode
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