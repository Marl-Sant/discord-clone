import Members from "../Members";
import SelectedChannel from '../SelectedChannel'
import Channels from "../Channels";
import EditAServerModal from "../EditAServer/EditAServerModal";
import { useState, useEffect, useContext } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useParams, useLocation, Redirect } from "react-router-dom";
import { useHistory } from "react-router-dom";
import { getAServer } from "../../store/servers";

const SelectedServer = () => {
    const [loaded, setLoaded] = useState(false);
    const [validated, setValidated] = useState(true);
    const { serverId, channelId} = useParams();
    const [channelLoaded, setChannelLoaded] = useState(false);

    const dispatch = useDispatch();
    const serversObj = useSelector((state) => state.serversReducer);
    const user = useSelector((state) => state.session.user);
    const membersObj = useSelector((state) => state.serversReducer.currentServer.members)
    const channelsObj = useSelector((state) => state.serversReducer.currentServer.channels)

    let history = useHistory();
    const [member, setMember] = useState(false);

    useEffect(() => {
        let membersArr;
        if (membersObj) membersArr = Object.values(membersObj);
        if (membersArr)
          setMember(membersArr.find((member) => member.userId === user.id));

          
        
        setLoaded(true);
        setChannelLoaded(true)
      // }, [membersObj, user.id, history, serverId]);
          }, [dispatch]);
      return (
        loaded && (
          <div>
            <div className="channels_container">
            {channelLoaded && (
              <Channels channels={channelsObj} className="channels" />
            )}
          </div>
          <div className="one_channel">
          {channelLoaded && (
            <SelectedChannel channelsObj={channelsObj} className="one_channel" />
          )}
        </div>

              <div className="members_container">
                <h1>MEMBERS</h1>
                {channelLoaded && (
                  <Members
                    serversObj={serversObj}
                    channelsObj={channelsObj}
                    className="members"
                  />
                )}
              </div>
              <EditAServerModal/>
          </div>
        )
      );
    };
    
    export default SelectedServer;
