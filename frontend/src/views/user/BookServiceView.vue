<script setup>
    import store from '@/store';
    import router from '@/router';
</script>
<template>
    <div class="billing-container">
        <h1>Billing Details</h1>
        <div class="bill">
            <p><strong>Service:</strong> {{ service_name }}</p>
            <p><strong>Price:</strong> ₹{{ service_price }}</p>

            <label for="booking-date"><strong>Select Date:</strong></label>
            <input id="booking-date" type="date" v-model="date" class="date-input" />
            <br />
            <label for="address"><strong>Enter Address:</strong></label>
            <input id="address" type="text" v-model="address" class="form-control" placeholder="Enter your address" />

            <label for="pincode"><strong>Enter Pincode:</strong></label>
            <input id="pincode" type="text" v-model="pincode" class="form-control" 
                   placeholder="Enter 6-digit pincode" maxlength="6" @input="validatePincode" />

            <p><strong>Total Amount:</strong> ₹{{ total_amount }}</p>


            <button class="btn btn-primary book-btn" @click="bookService">Book</button>
        </div>
    </div>
</template>



<script>
export default {
    created() {
        store.dispatch("getServices");
    },
    props: ['id'],
    data() {
        return {
            service_name: null,
            service_price: null,
            date: new Date().toISOString().split('T')[0], 
            total_amount: null,
            address: "",  
            pincode: ""   
        };
    },
    computed: {
        service() {
            return this.$store.getters.getServices.find(service => service.id === parseInt(this.id)) || null;
        }
    },
    watch: {
        service(value) {
            if (value) {
                this.service_name = value.name;
                this.service_price = value.price;
                this.total_amount = value.price;
            }
        }
    },
    methods: {
        validatePincode() {

            this.pincode = this.pincode.replace(/\D/g, "").slice(0, 6);
        },
        bookService() {
            if (!this.address || this.pincode.length !== 6) {
                alert("Please enter a valid address and 6-digit pincode.");
                return;
            }

            const bookingDetails = {
                service_name: this.service_name,
                service_price: this.service_price,
                date: this.date,
                address: this.address,
                pincode: this.pincode,
                total_amount: this.total_amount
            };

            fetch(import.meta.env.VITE_BASEURL + "/book_service", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": store.getters.getToken
                },
                body: JSON.stringify(bookingDetails)
            }).then(resp=>{
        
                return [resp.json(),resp.status]

            }).then(x=>{
                if(x[1]==200){
                    alert("Booking Successful.")
                    router.push(`/user`);
                }else{
                    alert("No Professionals available in this area.")
                    router.push(`/user/book/${id}`);
                }

            })
        }
    },
    mounted() {
        if (this.service) {
            this.service_name = this.service.name;
            this.service_price = this.service.price;
            this.total_amount = this.service.price;
        }
    }
};
</script>



<style scoped>
.billing-container {
    width: 50%;
    margin: auto;
    padding: 20px;
    border: 1px solid #ddd;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    background-color: #fff;
}
.bill p {
    font-size: 18px;
    margin: 10px 0;
}
.form-control {
    width: 100%;
    padding: 8px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
}
.book-btn {
    width: 100%;
    margin-top: 10px;
}
</style>

