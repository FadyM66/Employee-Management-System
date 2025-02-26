import useAuthContext from '../context/AuthContext';
import '../assets/style/username.css'


const Username = () => {

    const { name } = useAuthContext();

    return (
        <div id="username-btn">
            <p>{ name || null }</p>
        </div>
    );
};

export default Username;