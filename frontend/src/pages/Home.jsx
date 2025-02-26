import React, { useEffect, useState } from 'react';
import Logo from '../components/Logo.jsx';
import TopBar from '../components/TopBar.jsx';
import Username from '../components/SignoutBtn.jsx';
import '../assets/style/login.css';
import '../assets/style/companies.css'
import '../assets/style/home.css'
import { getData } from '../utils/utils.js';
import fetcher from '../utils/fetcher.js';
import useAuthContext from '../context/AuthContext.jsx';
import { useField } from 'formik';


const Home = () => {

    return (
        <>
            <TopBar />
            <div className='data-container'>
                <div className="upper-intro">
                    <h1>Summary</h1>
                    <p>Quick numbers about the organization</p>
                </div>
                <div className='summary-data'>
                    <h1> companies: </h1>
                    <h1> departments: </h1>
                    <h1> employees: </h1>
                    <h1> users: </h1>
                </div>
            </div>
        </>
    );
}

export default Home;