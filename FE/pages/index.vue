<template>
    <body>
        <div class=" mb-4 homeheader">
            <div class=" container pt-3">
                <div class=" row">
                    <div class=" col-4">
                    </div>
                    <div class=" col-1 offset-7">
                        <div class="dropdown">
                            <button class="btn color-btn btn-lg dropdown-toggle border border-light border-3" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
                                Action
                            </button>
                            <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="dropdownMenuButton1">
                                <li v-if="user_id == '70dcbac4-cfe9-4cb0-a68e-3d00fb31dfac'"><NuxtLink class="dropdown-item" to="/register-box">Register Box</NuxtLink></li>
                                <li><NuxtLink class="dropdown-item" to="/claim">Claim Box</NuxtLink></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><button class="dropdown-item logout-text" @click="goLogout()">Logout</button></li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class=" row mt-3">
                    <div class=" col greet-text d-flex align-items-center">
                        <h1>Good Morning, {{ user_name }}</h1>
                    </div>
                </div>
            </div>
        </div>

        <div class=" mt-4 homebody">
            <div class=" container">
                <div class=" row mb-4">
                    <div class=" col-12 text-center">
                        <h1>Boxes List</h1>
                    </div>
                </div>

                <div class=" row justify-content-center box-list" v-if="box_list[0]">
                    <NuxtLink :to="`/secretbox/` + box.box_id" class=" col-12 box-button align-items-center d-flex px-5 mb-3 justify-content-between" v-for="(box, index) in box_list" :key="index">
                        <div><h3>Box #{{ index+1 }}</h3></div>
                        <div><h1> 》 </h1></div>
                    </NuxtLink>
                </div>
                <div class=" row justify-content-center box-list" v-else>
                    <div class=" col-12 box-button px-5 mb-3 text-center d-flex align-items-center justify-content-center">
                        <div><h3>No Box Found</h3></div>
                    </div>
                </div>
            </div>
        </div>
    </body>
</template>

<script lang="ts">
const config = useRuntimeConfig();

export default {
    setup() {

    },
    data() {
        return {
            user_name: '',
            user_id: '',
            user_email: '',
            box_list: [{box_id: ''}],
            isUserLogged: false,
            isDev: config.public.WORK_TYPE
        }
    },
    methods: {
        dummyData() {
            this.user_name = 'manusia'
            this.user_id = '398c1422-e0e2-455a-875b-5a004a936f9c'
            this.user_email = 'manusia@mail.com'
            this.isUserLogged = true
            this.box_list = [
                {
                    box_id: 'c2647bb2-d87a-4489-a0db-5d7840abb36a'
                },
                {
                    box_id: '5086ea03-af16-46df-af11-de5d6a5b7569'
                }
            ]
        },
        cleanData() {
            this.user_name = ''
            this.user_id = ''
            this.user_email = ''
            this.isUserLogged = false
            this.box_list = [{box_id: ''}]
        },
        async cookieCheck() {
            const cookieVal = useCookie<string>('token');

            if(cookieVal.value == undefined) {
                navigateTo('/login');
            }

            const token = cookieVal.value;
            const requestOptions = {
                method: "GET",
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            };

            const result = await fetch('http://127.0.0.1:4000/auth/me', requestOptions);
            const resData = await result.json();
            
            this.user_name = resData.data.name;
            this.user_email = resData.data.email;
            this.user_id = resData.data.user_id;
            this.box_list = resData.data.boxes;
            this.isUserLogged = true
        },
        goLogout() {
            const cookieVal = useCookie('token');
            cookieVal.value = null;

            navigateTo('/login');
        }
    },
    beforeMount() {
        this.cookieCheck();
        // if(this.isDev == 'dev') {
        //     this.dummyData()
        // }
    }
}

</script>

<style scoped>
body {
    padding: 0;
    margin: 0;
}

.homeheader {
    background: rgb(25,55,254);
    background: linear-gradient(0deg, rgba(25,55,254,1) 0%, rgba(51,77,251,1) 42%, rgba(73,96,249,1) 100%);
    height: 40vh;
    margin-top: -40px;
    padding-top: 50px;
    border-radius: 50px;
}

.greet-text h1 {
    font-family: monospace;
    color: whitesmoke;
}

.box-list {
    padding: 0 10%;
}

.profile-btn {
    color: white;
}
.color-btn {
    background: rgb(65, 87, 235);
    color: white;
}

.logout-text {
    color: red;
}

.box-button {
    background: rgb(73,96,249);
    background: linear-gradient(90deg, rgba(73,96,249,1) 0%, rgba(47,74,252,1) 20%, rgba(20,51,255,1) 100%);
    border-radius: 40px;
    color: white;
    height: 10vh;
    text-decoration: none;
}

</style>