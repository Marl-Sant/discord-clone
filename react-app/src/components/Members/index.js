import "./Members.css";
import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Dispatch } from "react";

const Members = () => {
  const dispatch = useDispatch()
  const currentChannel = useSelector((state) => state.channelsReducer?.currentChannel);
  const currentServerMembers = useSelector(
    (state) => state.serversReducer?.currentServer?.members
  );

  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    if (currentChannel) {
      setLoaded(true);
    }
  }, [dispatch, currentChannel]);

  if (loaded && currentServerMembers) {
    return (
      <div className="members_list">
        {Object.values(currentServerMembers)?.map((member) => (
          <div className="member" key={member.id * 2}>
            <h4>{member.username}</h4>
          </div>
        ))}
      </div>
    );
  }

  return <h1>Loading...</h1>;
};

export default Members;
