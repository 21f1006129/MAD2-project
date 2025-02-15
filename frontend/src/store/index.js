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
            state.user = value;
        }
    }
})