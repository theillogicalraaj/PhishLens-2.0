const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
export function token(){return localStorage.getItem("phishlens_token")||"";}
export async function api<T>(path:string,options:RequestInit={}) : Promise<T>{
  const headers=new Headers(options.headers||{});
  headers.set("Content-Type", "application/json");
  const t=token(); if(t) headers.set("Authorization",`Bearer ${t}`);
  const r=await fetch(`${API}${path}`,{...options,headers});
  if(!r.ok){let d:any={}; try{d=await r.json()}catch{} throw new Error(d.detail||`Request failed (${r.status})`)}
  const type=r.headers.get("content-type")||"";
  if(type.includes("application/pdf")) return (await r.blob()) as T;
  return r.json();
}
export function saveToken(t:string){localStorage.setItem("phishlens_token",t)}
export function logout(){localStorage.removeItem("phishlens_token")}
export {API};
