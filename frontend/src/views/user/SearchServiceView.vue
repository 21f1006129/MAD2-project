<script setup>
    import store from '@/store';
    import router from '@/router';
</script>
<template>
  <div>
  <div class="d-flex justify-content-center my-3">
      <!-- 🔽 Dropdown to select search type -->
      <select v-model="searchType" class="form-select search-dropdown">
          <option value="service_name">Service Name</option>
          <option value="pincode">Pin Code</option>
      </select>

      <!-- 🔍 Search Input -->
      <input type="text" v-model="searchQuery" class="form-control search-input" placeholder="Enter search query..." style="max-width: 300px; margin-left: 10px"/>
  </div>

  <!-- 📋 Table of Services -->
  <table class="table">
      <thead>
          <tr>
              <th>#</th>
              <th>Name</th>
              <th>Price</th>
              <th>Description</th>
              <th>Action</th>
          </tr>
      </thead>
      <tbody>
          <tr v-for="(service, index) in filteredServices" :key="index">
              <th scope="row">{{ index + 1 }}</th>
              <td>{{ service.name }}</td>
              <td>₹{{ service.price }}</td>
              <td>{{ service.description }}</td>
              <td>
                  <button class="btn btn-primary" @click="redirect(service.id)">
                      Book
                  </button>
              </td>
          </tr>
      </tbody>
  </table>
</div>
</template>


<script>
export default {
    created() {
        store.dispatch("getServices");
        store.dispatch("getServiceProfessionals");
    },
    data() {
        return {
            searchQuery: "",  // User input for search
            searchType: "service_name"  // Default search type
        };
    },
    computed: {
        filteredServices() {
            const query = this.searchQuery.trim();
            if (!query) return this.$store.getters.getServices; // Show all if empty

            return this.searchType === "service_name"
                ? this.filterByServiceName(query)
                : this.filterByPincode(query);
        }
    },
    methods: {
        filterByServiceName(query) {
            return this.$store.getters.getServices.filter(service => 
                service.name.toLowerCase().includes(query.toLowerCase())
            );
        },
        filterByPincode(pincode) {
            if (!/^\d{6}$/.test(pincode)) return []; // Validate it's a 6-digit pin

            const professionals = this.$store.getters.getServiceProfessionals.filter(prof => 
                prof.pincode == pincode && prof.active == 1
            );

            const uniqueServices = new Set(professionals.map(prof => prof.service_type));
            console.log(professionals);

            return this.$store.getters.getServices.filter(service => 
                uniqueServices.has(service.name)
            );
        },
        redirect(id) {
            router.push(`/user/book/${id}`);
        }
    }
};
</script>


<style scoped>
.search-dropdown {
    width: 150px;
}
.search-input {
    flex-grow: 1;
}
</style>

