// import "./Members.css";
// import { useEffect, useState } from "react";
// import { useSelector, useDispatch } from "react-redux";
// //remember to return the passing prop serversObj
// const Members = () => {
//   const dispatch = useDispatch()
//   const serversMembers = useSelector((state) => state.serversReducer.currentServer.members)
//   const [loaded, setLoaded] = useState(true);
//   const [members, setMembers] = useState([]);
//   useEffect(() => {
//     let isActive = true;

//     setMembers(Object.values(serversMembers));
   
//     setLoaded(true);
//     return () => (isActive = false);
//   }, [dispatch, serversMembers]);

//   return (
//     loaded && (
//       <div className="members_list">
//         <h1>LIST OF MEMBERS</h1>
//         {members.map((member) => (
//           <div className="member" key={member.id}>
//             <h4>{member.username}</h4>
//           </div>
//         ))}
//       </div>
//     )
//   );
// };

// export default Members;

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
