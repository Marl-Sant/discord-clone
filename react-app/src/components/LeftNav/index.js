import "./LeftNav.css";
import Servers from "../Servers";
import { NavLink } from "react-router-dom";
import  CreateNewServerModal from "../CreateNewServer/CreateNewServerModal"
import { useSelector, useDispatch } from "react-redux";
import { getAChannel } from "../../store/channel";

const LeftNav = () => {
  const dispatch = useDispatch();
  const user = useSelector((state) => state.session.user)
  const userServers = useSelector((state) => state.session.user.serverMember)
  const handleHomeClick = async (channelId) => {
    await dispatch(getAChannel(channelId));
  };
  return (
    user && (
      <div className="left_side" id="left_nav">
        <NavLink
          className="home_dm_btn"
          to={`/discovery`}
        >
          <div className="icon_container">
            <img
              className="left_side_icon"
              src="/svgs/gray-disc-home.svg"
              alt="home"
            ></img>
          </div>
        </NavLink>
        <span className="home_seperator" />
        <Servers
          userServers={userServers}
        ></Servers>
        <CreateNewServerModal/>
      </div>
    )
  );
};

export default LeftNav;
