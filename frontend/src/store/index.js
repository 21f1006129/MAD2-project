import { createStore } from "vuex";

export default createStore({
    state(){
        return {
            user: {
                token: null,
                role: []
            },
            services: [],
            service_professionals: [],
            customers: [] 
        }
    },
    mutations:{
        setUser(state,value){
            localStorage.setItem("user", JSON.stringify(value));
            state.user = value;
        },
        setServices(state,value){
            state.services = value;
        },
        setServiceProfessionals(state,value){
            state.service_professionals = value;
        },
        setCustomers(state,value){
            state.customers = value;
        }
    },
    getters: {
        getRoles(state){
            if (state.user['role']){
                return state.user['role']
            }

            return [];
        },
        getToken(state){
            if (state.user['token']){
                return state.user['token']
            }
            return null;
        },
        getService(state){
            return state.services
        },
        getServiceProfessionals(state){
            return state.service_professionals 
        },
        getCustomers(state){
            return state.customers
        }
    },
    actions: {
       getServices({commit,state}){
            fetch(import.meta.env.VITE_BASEURL + "/service", {
                method: "GET",
                headers: {
                  "Authentication-Token": state.user["token"],
            
                }
              }).then(response => response.json()).then(x =>{
                commit("setServices",x)

            } )
        } ,
        getServiceProfessionals({commit,state}){
            fetch(import.meta.env.VITE_BASEURL + "/service_professionals", {
                method: "GET",
                headers: {
                  "Authentication-Token": state.user["token"],
            
                }
              }).then(response => response.json()).then(x =>{
                commit("setServiceProfessionals",x)

            } )
        },
        getCustomers({commit,state}){
            fetch(import.meta.env.VITE_BASEURL + "/customers", {
                method: "GET",
                headers: {
                  "Authentication-Token": state.user["token"],
            
                }
              }).then(response => response.json()).then(x =>{
                commit("setCustomers",x)

            } )
        }
    }
})