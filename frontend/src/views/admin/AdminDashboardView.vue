<script>
import store from '@/store';

export default {
    data() {
        return {
            serviceRequests: [],
            filteredRequests: [],
            selectedStatus: "All", 
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
                this.filterRequests(); 
            })
            .catch(error => console.error("Error fetching service requests:", error));
        },
        filterRequests() {
            if (this.selectedStatus === "All") {
                this.filteredRequests = this.serviceRequests;
            } else {
                this.filteredRequests = this.serviceRequests.filter(request => 
                    request.service_status === this.selectedStatus);
            }
        }
    }
};
</script>

<template>
    <div class="admin-dashboard">
        <h1>Welcome Admin: Thanos</h1>

        <div class="filter-container">
            <label for="statusFilter">Search:</label>
            <select v-model="selectedStatus" @change="filterRequests">
                <option value="All">All</option>
                <option value="pending">Pending</option>
                <option value="assigned">Assigned</option>
                <option value="completed">Completed</option>
            </select>
        </div>

        <div v-if="filteredRequests.length > 0">
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
                    <tr v-for="(request, index) in filteredRequests" :key="request.id">
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
.filter-container {
    margin-bottom: 15px;
}
.filter-container label {
    font-weight: bold;
    margin-right: 10px;
}
.filter-container select {
    padding: 5px;
    font-size: 16px;
}
.table {
    width: 100%;
    margin-top: 20px;
    border-collapse: collapse;
}
</style>
