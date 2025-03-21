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
                    <input type="password" class="form-control" v-model="password" placeholder="password" aria-label="password" required >
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
                        <input type="text" class="form-control" v-model="pincode"
                            maxlength="6" minlength="6" pattern="^\d{6}$"
                            @input="pincode = pincode.replace(/\D/g, '')"
                            required placeholder="Enter 6-digit pincode">
                    </div>
                </div>
                <div class="row">
                    <p>Select Service Type</p>
                    <select class="form-select form-select-sm" v-model ="service_type" aria-label="Small select example">
                        <option v-for="(service, index) in store.getters.getService" :key="index" :value="service.name">
                            {{ service.name }}
                        </option>
                    </select>

                </div>
                <div class="row">
                    <div class="col">
                        <input type="file" ref="pdf_input" class="form-control" @change="handleFileUpload" accept="application/pdf" required>
                    </div>
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
        created(){
            store.dispatch("getServices")
        },
        data(){
            return {
                fullname: null,
                username : null,
                password : null,
                confirm_password : null,
                service_type : null,
                pincode : null,
                pdfFile:null,
                error : {
                    username : null,
                    password : null
                },
                message : null,
                message1 : null
                
            }
        },
        methods:{
            validate() {
                this.message = null;
                this.message1 = null;

                // Check for empty fields
                if (!this.fullname || !this.username || !this.password || !this.confirm_password || !this.pincode || !this.service_type) {
                    this.message1 = 'Please fill all the required fields.';
                    return false; // Stop form submission
                }

                // Check if passwords match
                if (this.password !== this.confirm_password) {
                    this.message1 = "Passwords don't match.";
                    return false;
                }

                // Check if pincode is exactly 6 digits
                if (String(this.pincode).length !== 6) {
                    this.message1 = 'Pincode must be 6 digits long.';
                    return false;
                }

                // Check if PDF file is uploaded
                if (!this.pdfFile) {
                    this.message1 = 'Please upload a PDF file.';
                    return false;
                }

                // Optionally check if uploaded file is a PDF (MIME type check)
                if (this.pdfFile.type !== 'application/pdf') {
                    this.message1 = 'Uploaded file must be a PDF.';
                    return false;
                }
                return true;
            },
            resetForm() {
                this.fullname = null;
                this.username = null;
                this.password = null;
                this.confirm_password = null;
                this.pincode = null;
                this.service_type = null;
                this.pdfFile = null; 
                this.$refs.pdf_input.value = null;
            },
            handleFileUpload(event) {
                this.pdfFile = event.target.files[0]; 
                console.log('Selected file:', this.pdfFile);
            },  
            signup() {
                this.validate();
                
                const formData = new FormData();
                formData.append('fullname', this.fullname);
                formData.append('username', this.username);
                formData.append('password', this.password);
                formData.append('pincode', this.pincode);
                formData.append('service_type', this.service_type);
                formData.append('pdfFile', this.pdfFile); 

                fetch(import.meta.env.VITE_BASEURL + '/servicepro-signup', {
                    method: 'POST',
                    body: formData 
                })
                .then(resp => [resp.json(), resp.status])
                .then(([data, status]) => {
                    console.log('Response status:', status);
                    console.log(data['message'])
                    if (status === 200) {
                        this.message1 = null;
                        this.message = 'Signup successful! Please login.';
                        this.pdfFile = null;
                        this.resetForm();
                        router.push({ path: "/servicepro-signup" });
                    } else if (status ===409) {
                        this.message = null;
                        this.message1 = 'Username already Exists.';
                        this.resetForm();
                        router.push({ path: "/servicepro-signup" });
                    
                    }else {
                        this.message = null;
                        this.message1 = 'Invalid Form Response';
                        this.resetForm();
                        router.push({ path: "/servicepro-signup" });
                    }
                });
            }
        },
        computed:{
            toggle(){
                if(this.password == this.confirm_password || this.password == '' || this.confirm_password == ''){
                    return ''
                }
                return "Passwords don't match."
            },

        }
     }
</script>

<style scoped>
     .container-fluid{
        width:90%;
        height:110vh;
        overflow: hidden;
        display:flex;
        justify-content: center;
        align-items: center;
     }
     .row{
        padding: 10px;
     }
</style>