import useAuthContext from '../context/AuthContext';
import { signoutClearCookies } from '../utils/handlers.js';
import '../assets/style/signoutBtn.css'

const SignoutBtn = () => {

    const { isLoggedIn, setToken, setEmail, setName } = useAuthContext();

    return (
        <>
            <div id="Signout-btn">
                {
                    isLoggedIn ?
                <p onClick={() => {
                    signoutClearCookies()
                    setToken(null);
                    setEmail(null);
                    setName(null);
                    }}>Sign out</p>
                    :
                null
                }
            </div>
        </>
    )
}

export default SignoutBtn;