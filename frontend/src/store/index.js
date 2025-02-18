import { createStore } from "vuex";

export default createStore({
    state(){
        return {
            user: {
                token: null,
                role: []
            }
        }
    },
    mutations:{
        setUser(state,value){
            localStorage.setItem("user", JSON.stringify(value));
            state.user = value;
        }
    },
    getters: {
        getRoles(state){
            return state.user['role'];
        }
    }
})