import SelectedServer from "../SelectedServer";
import { useContext, useEffect, useState } from "react";
import { Route, Switch } from "react-router-dom";

const MainView = ({ user }) => {
    // const { dmRoomsView, setDmRoomsView } = useContext(DmRoomViewContext);
    // let url = useLocation();

    return (
          <div>
          <h1>MAINVIEW</h1>
            <Switch>
              <Route
                path="/channels/:serverId/:channelId"
                exact={true}
              >
                <SelectedServer />
              </Route>
              {/* <ProtectedRoute path="/channels/wampus/404" exact={true}>
                <Wampus />
              </ProtectedRoute>
              <ProtectedRoute path="/channels/*">
                <Wampus />
              </ProtectedRoute> */}
            </Switch>
          </div>
      );
    };
    
    export default MainView;
