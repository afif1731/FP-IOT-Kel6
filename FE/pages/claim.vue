<template>
    <div class="login-container">
      <div class="login-box">
        <h2>Claim Box</h2>
        <form @submit.prevent="handleClaim">
          <div class="form-group">
            <label for="boxid">Box Id:</label>
            <input type="text" id="boxid" v-model="boxid" required>
          </div>
          <div class="form-group">
            <label for="password">Box Password:</label>
            <input type="password" id="password" v-model="password" required>
          </div>
          <button type="submit" class="login-button">Claim</button>
        </form>
      </div>
    </div>
  </template>

  <script>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import { useCookie } from '#app';
  
  export default {
    name: 'Claim Box',
    setup() {
      const router = useRouter();
      const boxid = ref('');
      const password = ref('');
  
      const handleClaim = async() => {
        const cookieVal = useCookie('token');

        if(cookieVal.value == undefined) {
            navigateTo('/login');
        }
        const token = cookieVal.value;

        if (boxid.value && password.value) {
          const submitData = {
            password: password.value
          }

          const requestOptions = {
            method: "POST",
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(submitData)
          };

          const result = await fetch(`http://127.0.0.1:4000/secretbox/${boxid.value}/claim`, requestOptions);
          const resData = await result.json();

          if (resData.status) {
            router.push('/');
          } else {
            alert(resData.message);
          }
        }
      };
  
      return {
        boxid,
        password,
        handleClaim,
      };
    },
    mounted() {
      const cookieVal = useCookie('token');

      if(cookieVal.value == undefined) {
          navigateTo('/login');
      }
    }
  };
  </script>
  
  <style scoped>
  .login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background: linear-gradient(135deg, #f3f4f7, #e2e2e2);
  }
  
  .login-box {
    background: white;
    padding: 2em 2em 1em 2em;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 400px;
    text-align: center;
  }
  
  h2 {
    margin-bottom: 1em;
    color: #333;
  }
  
  .form-group {
    margin-bottom: 1em;
    text-align: left;
  }
  
  label {
    display: block;
    margin-bottom: 0.5em;
    color: #555;
  }
  
  input[type="text"],
  input[type="password"] {
    width: 100%;
    padding: 0.75em;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 1em;
  }
  
  input[type="text"]:focus,
  input[type="password"]:focus {
    border-color: #007bff;
    outline: none;
    box-shadow: 0 0 5px rgba(0, 123, 255, 0.25);
  }
  
  .login-button {
    display: inline-block;
    width: 100%;
    padding: 0.75em;
    background-color: #007bff;
    border: none;
    border-radius: 4px;
    color: white;
    font-size: 1em;
    cursor: pointer;
  }
  
  .login-button:hover {
    background-color: #0056b3;
  }
  
  .login-button:focus {
    outline: none;
    box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
  }
  </style>
  