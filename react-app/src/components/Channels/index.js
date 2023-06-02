import "./Channels.css";
import { NavLink } from "react-router-dom";
import { getAChannel } from "../../store/channel";
import { useDispatch, useSelector } from "react-redux";
import { useParams, useLocation } from "react-router-dom";
import { useState, useEffect } from "react";


const Channels = () => {
    const { channelId, dmRoomId } = useParams();

    const [ownerId, setOwnerId] = useState();
    const [currentChannelId, setCurrentChannelId] = useState(channelId);
    const [hoverId, setHoverId] = useState(null);
    const [channels, setChannels] = useState();
    // const [showServerOptions, setShowServerOptions] = useState(false)
    const user = useSelector((state) => state.session.user);
    const currentServer = useSelector((state) => state.serversReducer.currentServer);
    const channelsObj = useSelector((state) => state.serversReducer.currentServer.channels);
    const dispatch = useDispatch();
    useEffect(() => {
        setOwnerId(currentServer?.owner?.id);
        setChannels(Object.values(channelsObj))
    }, [
        dispatch,
        currentServer,
        setOwnerId,
        channelsObj,
        channelId,
    ]);

    const handleChannelChange = async (channelId) => {
        await dispatch(getAChannel(channelId)).then(() =>
            setCurrentChannelId(channelId)
        );
    };
    return (
        <div className="channels">
            <div className="channels_header">
                <h1>ALL CHANNELS</h1>
            </div>

            {channels?.map((channel) => (
                <NavLink
                    key={channel.id}
                    to={
                        `/channels/${channel.serverId}/${channel.id}`
                    }
                    onClick={() => handleChannelChange(channel.id)}
                >
                    <div
                        className="channel"
                        onMouseEnter={() => setHoverId(channel.id)}
                        onMouseLeave={() => setHoverId(null)}
                    >
                        {/* <div className="channel_left">
              <img
                className={`${dmRoomsView && "direct_message_icon"}`}
                src={
                  dmRoomsView
                    ? Object.keys(channel?.members).length > 2
                      ? "/svgs/group-message-ico.svg"
                      : Object.values(channel.members)[0]?.profilePicture
                    : "/svgs/pound.svg"
                }
                alt="#"
              />
              {" "}
              {dmRoomsView ? (
                Object.values(channel.members).map((member) => (
                  <p key={member.id}>{member.username}</p>
                ))
                ) : (
                    )}
                </div> */}
                        {((ownerId === user.id && currentChannelId * 1 === channel.id) ||
                            (ownerId === user.id && hoverId === channel.id)) &&
                            channel.name !== "General Chat" &&
                            !channelsObj.currentChannel.dmChannel && (
                                <div className="channel_right">
                                    {/* <img src="/svgs/addMemb.svg" alt="add" /> */}
                                    {/* <EditChannelModal channel={channel} user={user} /> */}
                                </div>
                            )}
                            <p>{channel.name}</p>
                    </div>
                </NavLink>
            ))}
        </div>
    );
};

export default Channels;
