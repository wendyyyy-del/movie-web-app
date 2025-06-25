import React, { useState } from 'react';
import axios from 'axios';
import '../style.css';

const Login = () => {
  const [form, setForm] = useState({ username: '', password: '' });
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleLogin = async () => {
    try {
      const res = await axios.post('http://localhost:5000/api/auth/login', form);
      localStorage.setItem('token', res.data.token); // Assuming Flask returns 'token'
      localStorage.setItem('username', form.username);
      window.location.href = '/dashboard';
    } catch (err) {
      setError('Login failed. Check your credentials.');
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2 className="login-title">Sign In</h2>

        <label htmlFor="username">Username</label>
        <input
          name="username"
          id="username"
          value={form.username}
          onChange={handleChange}
          placeholder="Enter your username"
        />

        <label htmlFor="password">Password</label>
        <input
          name="password"
          id="password"
          type="password"
          value={form.password}
          onChange={handleChange}
          placeholder="Enter your password"
        />

        <button onClick={handleLogin}>Sign In</button>

        {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}

        <p className="login-footer">
          New to MovieApp? <a href="/register">Sign up now</a>
        </p>
      </div>
    </div>
  );
};

export default Login;
