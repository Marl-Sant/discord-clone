import "./SelectedChannel.css";
import Messages from "../Messages";
import { useSelector } from "react-redux";
import { postMessage } from "../../store/channel";
import { useDispatch } from "react-redux";
import { useState, useEffect } from "react";
// maybe pass in an object from SelectedServer?
const SelectedChannel = () => {
  const currentChannel = useSelector((state) => state.channelsReducer.currentChannel);
  const channelId = currentChannel?.id;
  const [messages, setMessages] = useState([]);

  const dispatch = useDispatch();

  useEffect(() => {
    let isActive = true;
    const channelMessagesObj = currentChannel?.messages;

    if (channelMessagesObj && isActive)
      setMessages(Object.values(channelMessagesObj));

    return () => (isActive = false);
  }, [currentChannel]);


  return (
    <>
    <h1>CURRENT CHANNEL</h1>
    {currentChannel?.messages && <Messages messages={messages} />}
    </>
  );
};

export default SelectedChannel;
