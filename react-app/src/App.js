import React, { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { Route, Switch } from "react-router-dom";
import DiscoveryPage from './components/DiscoveryPage'
import MainView from "./components/MainView";
import SelectedServer from "./components/SelectedServer";
import Members from "./components/Members";
import SignupFormPage from "./components/SignupFormPage";
import LoginFormPage from "./components/LoginFormPage";
import { authenticate } from "./store/session";
import Navigation from "./components/Navigation";

function App() {
  const dispatch = useDispatch();
  const [isLoaded, setIsLoaded] = useState(false);
  const user = useSelector((state) => state.session.user);
  useEffect(() => {
    dispatch(authenticate()).then(() => setIsLoaded(true));
  }, [dispatch]);

  return (
    <>
      <Navigation isLoaded={isLoaded} />
      {isLoaded && (
        <Switch>
          <Route path="/login" >
            <LoginFormPage />
          </Route>
          <Route path="/signup">
            <SignupFormPage />
          </Route>
          <Route path="/discovery">
            <DiscoveryPage />
          </Route>
          <Route path="/channels">
            <MainView />
            {/* <SelectedServer /> */}
            {/* <Members /> */}
          </Route>
        </Switch>
      )}
    </>
  );
}

export default App;
