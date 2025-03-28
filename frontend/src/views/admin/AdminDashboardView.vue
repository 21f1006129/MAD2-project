<script>
import store from '@/store';

export default {
    data() {
        return {
            serviceRequests: [],
        };
    },
    created() {
        this.fetchServiceRequests();
    },
    methods: {
        fetchServiceRequests() {
            fetch(import.meta.env.VITE_BASEURL + "/service_requests/all", {
                method: "GET",
                headers: {
                    "Authentication-Token": store.getters.getToken
                }
            })
            .then(response => response.json())
            .then(data => {
                this.serviceRequests = data;
            })
            .catch(error => console.error("Error fetching service requests:", error));
        }
    }
};
</script>

<template>
    <div class="admin-dashboard">
        <h1>Welcome Admin: Thanos</h1>

        <div v-if="serviceRequests.length > 0">
            <h2>All Service Requests</h2>
            <table class="table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Service ID</th>
                        <th>Service Name</th>
                        <th>User ID</th>
                        <th>Professional ID</th>
                        <th>Date of Request</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(request, index) in serviceRequests" :key="request.id">
                        <td>{{ index + 1 }}</td>
                        <td>{{ request.id }}</td>
                        <td>{{ request.service_name }}</td>
                        <td>{{ request.user_id }}</td>
                        <td>{{ request.professional_id }}</td>
                        <td>{{ request.date_of_request }}</td>
                        <td>{{ request.service_status }}</td>
                    
                    </tr>
                </tbody>
            </table>
        </div>
        <p v-else>No service requests found.</p>
    </div>
</template>

<style scoped>
.admin-dashboard {
    width: 80%;
    margin: auto;
    padding: 20px;
}
.table {
    width: 100%;
    margin-top: 20px;
    border-collapse: collapse;
}
</style>
