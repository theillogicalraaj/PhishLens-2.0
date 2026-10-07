import {Link,useNavigate} from "react-router-dom";
import {logout} from "../services/api";
export default function Layout({children}:{children:React.ReactNode}){
 const nav=useNavigate(); return <div className="shell"><aside><div className="brand">PHISHLENS<span>2.0</span></div><p className="muted">Security Awareness Intelligence</p><nav><Link to="/">Dashboard</Link><Link to="/campaigns">Campaigns</Link><Link to="/campaigns/new">New Campaign</Link></nav><button className="ghost" onClick={()=>{logout();nav('/login')}}>Sign out</button></aside><main>{children}</main></div>
}
