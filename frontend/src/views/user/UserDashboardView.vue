<script>
import store from '@/store';
import router from '@/router';

export default {
    data() {
        return {
            pendingRequests: [],
            completedRequests: [],
        };
    },
    created() {
        this.fetchServiceRequests();
    },
    methods: {
        fetchServiceRequests() {
            fetch(import.meta.env.VITE_BASEURL+`/service_requests/user`, {
                method: "GET",
                headers: {
                    "Authentication-Token": store.getters.getToken
                }
            })
            .then(response => response.json())
            .then(data => {
                
                this.pendingRequests = data.filter(req => req.service_status === "pending" || req.service_status === "assigned");
                this.completedRequests = data.filter(req => req.service_status === "completed");
            })
            .catch(error => console.error("Error fetching service requests:", error));
        },
        closeRequest(id) {
            fetch(import.meta.env.VITE_BASEURL+`/close_service/${id}`, {
                method: "PATCH",
                headers: {
                    "Authentication-Token": store.getters.getToken
                }
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                router.push(`/user/feedback/${id}`); 
            })
            .catch(error => {
                console.error("Error closing service request:", error);
                alert("Error closing service request. Please try again.");
            });
        },
        bookAgain(id) {
            fetch(import.meta.env.VITE_BASEURL+`/delete_service_request/${id}`, {
                method: "DELETE",
                headers: {
                    "Authentication-Token": store.getters.getToken
                }
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                router.push("/user/search"); 
            })
            .catch(error => {
                console.error("Error deleting request:", error);
                alert("Error deleting request. Please try again.");
            });
        },
        cancelRequest(id) {
            fetch(import.meta.env.VITE_BASEURL+`/delete_service_request/${id}`, {
                method: "DELETE",
                headers: {
                    "Authentication-Token": store.getters.getToken
                }
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                this.fetchServiceRequests(); 
            })
            .catch(error => {
                console.error("Error canceling request:", error);
                alert("Error canceling request. Please try again.");
            });
        },
        rateService(id) {
            router.push(`/user/feedback/${id}`);
        }
    }
};
</script>

<template>
    <div class="dashboard-container">
        <h1>Welcome to Household Services, Book your service now.</h1>

        
        <div v-if="pendingRequests.length > 0">
            <h2>Pending Service Requests</h2>
            <table class="table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Service Name</th>
                        <th>Service Professional</th>
                        <th>Date</th>
                        <th>Address</th>
                        <th>Pincode</th>
                    
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(request, index) in pendingRequests" :key="request.id">
                        <td>{{ index + 1 }}</td>
                        <td>{{ request.service_name }}</td>
                        <td>{{ request.professional_id || "None available please book with another date"}}</td>
                        <td>{{ request.date_of_request }}</td>
                        <td>{{ request.address }}</td>
                        <td>{{ request.pincode }}</td>
                        <td>
                            <button v-if="request.professional_id" class="btn btn-success" @click="closeRequest(request.id)">
                                Close
                            </button>
                            <button v-else class="btn btn-warning" @click="bookAgain(request.id)">
                                Book Again
                            </button>
                        </td>
                        <td>
                            <button class="btn btn-danger" @click="cancelRequest(request.id)">
                                Cancel
                            </button>
                        </td>
                        
                    </tr>
                </tbody>
            </table>
        </div>
        <p v-else>No pending requests yet.</p>

        
        <div v-if="completedRequests.length > 0">
            <h2>Completed Service Requests</h2>
            <table class="table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Service Name</th>
                        <th>Professional id</th>
                        <th>Date</th>
                        <th>Address</th>
                        <th>Pincode</th>
                        <th>Feedback</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(request, index) in completedRequests" :key="request.id">
                        <td>{{ index + 1 }}</td>
                        <td>{{ request.service_name }}</td>
                        <td>{{ request.professional_id }}</td>
                        <td>{{ request.date_of_request }}</td>
                        <td>{{ request.address }}</td>
                        <td>{{ request.pincode }}</td>
                        <td>{{ request.feedback || "No feedback given" }}</td>
                        <td>
                            <button class="btn btn-primary" v-if="request.rating == null" @click="rateService(request.id)">
                                Rate this service
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <p v-else>No completed requests yet.</p>
    </div>
</template>

<style scoped>
.dashboard-container {
    width: 80%;
    margin: auto;
    padding: 20px;
}
.table {
    width: 100%;
    margin-top: 20px;
    border-collapse: collapse;
}
.btn-success {
    padding: 5px 10px;
    cursor: pointer;
}
</style>
