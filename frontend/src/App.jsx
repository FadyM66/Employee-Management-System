import useAuthContext, { AuthContextProvider } from './context/AuthContext.jsx';
import Logo from './components/Logo.jsx';
import Username from './components/Username.jsx';
import Home from './pages/Home.jsx';
import Login from './pages/Login';
import SignoutBtn from './components/SignoutBtn.jsx';
import './assets/style/general.css';
import './assets/style/common.css';

/** 
 *   The Layout is a bridge, so we can use the context inside the context provider at the App component.
 */

function App() {

  return (
     <>
        <AuthContextProvider>
          <Layout />
        </AuthContextProvider>
      </>
    );
}

function Layout() {

  const { isLoggedIn, name } = useAuthContext();

  return (
    <>
      <Logo />
      <Username />
      {isLoggedIn ? <Home /> : <Login />}
      <SignoutBtn />
    </>
  );
}

export default App;
