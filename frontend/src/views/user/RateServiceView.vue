<script>
import store from '@/store';
import router from '@/router';

export default {
    props: ['id'], 
    data() {
        return {
            service_name: "",
            rating: null,
            feedback: ""
        };
    },
    created() {
        this.fetchServiceDetails();
    },
    methods: {
        fetchServiceDetails() {
            fetch(import.meta.env.VITE_BASEURL+`/service_request/${this.id}`, {
                method: "GET",
                headers: {
                    "Authentication-Token": store.getters.getToken
                }
            })
            .then(response => response.json())
            .then(data => {
                this.service_name = data.service_name;
            })
            .catch(error => console.error("Error fetching service request:", error));
        },
        submitFeedback() {
            if (!this.rating) {
                alert("Please select a rating.");
                return;
            }

            const feedbackData = {
                rating: this.rating,
                feedback: this.feedback
            };

            fetch(import.meta.env.VITE_BASEURL+`/submit_feedback/${this.id}`, {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": store.getters.getToken
                },
                body: JSON.stringify(feedbackData)
            })
            .then(response => response.json())
            .then(data => {
                console.log(data["message"])
                alert("Feedback submitted successfully!");
                router.push("/user"); 
            })
            .catch(error => {
                console.error("Error submitting feedback:", error);
                alert("Error submitting feedback. Please try again.");
            });
        }
    }
};
</script>

<template>
    <div class="feedback-container">
        <h1>Rate Your Service</h1>
        <div class="feedback-card">
            <p><strong>Service:</strong> {{ service_name }}</p>

            <label><strong>Rating:</strong></label>
            <select v-model="rating" class="form-select">
                <option disabled value="">Select Rating</option>
                <option v-for="n in 5" :key="n" :value="n">{{ n }}</option>
            </select>

            <label><strong>Feedback:</strong></label>
            <textarea v-model="feedback" class="form-control" placeholder="Write your feedback here..."></textarea>

            <button class="btn btn-primary submit-btn" @click="submitFeedback">Submit</button>
        </div>
    </div>
</template>

<style scoped>
.feedback-container {
    width: 50%;
    margin: auto;
    padding: 20px;
}
.feedback-card {
    border: 1px solid #ddd;
    padding: 15px;
    border-radius: 5px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
}
.form-select, .form-control {
    width: 100%;
    margin-bottom: 10px;
    padding: 8px;
}
.submit-btn {
    width: 100%;
    margin-top: 10px;
}
</style>
