<script>
import store from '@/store';

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
            fetch(import.meta.env.VITE_BASEURL+"/service_requests/professional", {
                method: "GET",
                headers: {
                    "Authentication-Token": store.getters.getToken
                }
            })
            .then(response => response.json())
            .then(data => {
                this.pendingRequests = data.filter(req => req.service_status === "pending");
                this.completedRequests = data.filter(req => req.service_status === "completed");
            })
            .catch(error => console.error("Error fetching service requests:", error));
        },
        rejectRequest(id) {
            fetch(import.meta.env.VITE_BASEURL+`/reject_service/${id}`, {
                method: "PATCH",
                headers: {
                    "Authentication-Token": store.getters.getToken
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log(data.message);
                this.fetchServiceRequests(); 
            })
            .catch(error => {
                console.error("Error rejecting request:", error);
                alert("Error rejecting request. Please try again.");
            });
        }
    }
};
</script>

<template>
    <div class="dashboard-container">
        <h1>Service Professional Dashboard</h1>

        <!-- Pending Service Requests Table -->
        <div v-if="pendingRequests.length > 0">
            <h2>Pending Service Requests</h2>
            <table class="table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Service Name</th>
                        <th>Date</th>
                        <th>Address</th>
                        <th>Pincode</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(request, index) in pendingRequests" :key="request.id">
                        <td>{{ index + 1 }}</td>
                        <td>{{ request.service_name }}</td>
                        <td>{{ request.date_of_request }}</td>
                        <td>{{ request.address }}</td>
                        <td>{{ request.pincode }}</td>
                        <td>
                            <button class="btn btn-danger" @click="rejectRequest(request.id)">
                                Reject
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <p v-else>No pending requests yet.</p>

        <!-- Completed Service Requests Table -->
        <div v-if="completedRequests.length > 0">
            <h2>Completed Service Requests</h2>
            <table class="table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Service Name</th>
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
                        <td>{{ request.date_of_request }}</td>
                        <td>{{ request.address }}</td>
                        <td>{{ request.pincode }}</td>
                        <td>{{ request.feedback || "No feedback given" }}</td>
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
.btn-danger {
    background-color: red;
    color: white;
    border: none;
    padding: 5px 10px;
    cursor: pointer;
}
</style>
