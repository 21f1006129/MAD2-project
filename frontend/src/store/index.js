import { createStore } from "vuex";

export default createStore({
    state(){
        return {
            user: {
                token: null,
                role: []
            },
            services: [],
        }
    },
    mutations:{
        setUser(state,value){
            localStorage.setItem("user", JSON.stringify(value));
            state.user = value;
        },
        setServices(state,value){
            state.services = value;
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
        }
    }
})