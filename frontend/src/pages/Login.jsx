import { useEffect } from 'react';
import useAuthContext from '../context/AuthContext.jsx';
import InputRow from '../components/InputRow.jsx';
import { useLoginForm } from '../utils/validators.js';
import '../assets/style/login.css';


const Login = () => {

    const { setToken, setEmail, setName } = useAuthContext();

    const {
        values,
        errors,
        touched,
        isSubmitting,
        handleChange,
        handleBlur,
        handleSubmit,
        submissionResult
      } = useLoginForm();

    useEffect (()=>{
        if (submissionResult){
            setToken(submissionResult.token)
            setEmail(submissionResult.email)
            setName(submissionResult.name)}      
    },[submissionResult])

    return (
        <>            
            <div className="login-card">
                <div className="login-text">
                    <h1 className='prompt-h1'>Sign in</h1>
                    <p className='prompt-p'>Welcome back! Please sign in to continue</p>
                </div>
                <div className="form-container">
                    <form onSubmit={handleSubmit}>
                        <InputRow
                            values={values}
                            handleChange={handleChange}
                            handleBlur={handleBlur}
                            errors={errors}
                            touched={touched}
                            htmlFor="email"
                            label="Email"
                            inputId="login-email"
                            name="email"
                            type="email"
                            placeholder="Enter an Email"
                        />
                        <InputRow
                            values={values}
                            handleChange={handleChange}
                            handleBlur={handleBlur}
                            errors={errors}
                            touched={touched}
                            htmlFor="login-password"
                            label="Password"
                            inputId="login-password"
                            name="password"
                            type="password"
                            placeholder="Enter your password"
                        />
                        <button id='signin-btn' type="submit">
                            <span>{isSubmitting ? "Signning in" : 'Sign in'}</span>
                        </button>
                    </form>
                </div>
            </div>
        </>
    );
}

export default Login;