import axios from './index';

export default{
    getStoreObject() {
        return axios.get(`stored-objects/`)
            .then(response => {
                // JSON responses are automatically parsed.
                return response.data;
            })
            .catch((e) => {
                console.log(e)
                return e;
            });
    },

    addStoreObject(param) {
        return axios.post(`stored-objects/`,param)
            .then(response => {
                // JSON responses are automatically parsed.
                return response.data;
            })
            .catch((e) => {
                console.log(e)
                return e;
            });
    },

    getStoreObjectByUUID(uuid) {
        return axios.get(`stored-objects/${uuid}/`)
            .then(response => {
                // JSON responses are automatically parsed.
                return response.data;
            })
            .catch((e) => {
                console.log(e)
                return e;
            });
    },

    updateStoreObjectByUUID(uuid,param) {
        return axios.put(`stored-objects/${uuid}/`, param)
            .then(response => {
                // JSON responses are automatically parsed.
                return response.data;
            })
            .catch((e) => {
                console.log(e)
                return e;
            });
    }
}