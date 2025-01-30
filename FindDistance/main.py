import streamlit as st
import osmnx as ox
import networkx as nx
import folium



st.title("Find Distance Point")


def test2(x1,x2,y1,y2):
    G_drive = ox.graph_from_point((x1,x2), dist=20000, network_type="drive_service") # ดาวน์โหลดเครือข่ายถนนในรัศมีที่ใหญ่ขึ้นเพื่อให้ครอบคลุมทั้งจุดเริ่มต้นและปลายทาง
    orig_node = ox.distance.nearest_nodes(G_drive, x2, x1)
    dest_node = ox.distance.nearest_nodes(G_drive, y2 ,y1)
    route = nx.shortest_path(G_drive, orig_node, dest_node, weight="length")
    route_length_meters = nx.shortest_path_length(G_drive, orig_node, dest_node, weight="length")
    route_length_km = route_length_meters / 1000

    edges = ox.graph_to_gdfs(G_drive, nodes=False, edges=True)
    m = folium.Map(location=(x1,x2), zoom_start=14, tiles="CartoDB Positron")
    route_coords = [(G_drive.nodes[n]['y'], G_drive.nodes[n]['x']) for n in route]
    folium.PolyLine(route_coords, color="blue", weight=5, opacity=0.7).add_to(m)

    folium.Marker((x1,x2), popup="จุดเริ่มต้น", icon=folium.Icon(color="green")).add_to(m)
    folium.Marker((y1,y2), popup="จุดปลายทาง", icon=folium.Icon(color="red")).add_to(m)

    #fig, ax = ox.plot_graph_route(G_drive, route, route_linewidth=6, node_size=0, bgcolor='k')
    m.save("map.html")
    st.write("Route Length (Km):", route_length_km)
    with open("map.html", "r",encoding='utf-8') as f:
        map_html = f.read()
    st.components.v1.html(map_html, height=600)
    



def test():
    Point1 = st.text_input("Enter a origin:", placeholder="(Latitude, Longitude)", key="Point1")
    Point2 = st.text_input("Enter a destination:", placeholder="(Latitude, Longitude)")
    submit_button = st.button("Submit")

    if submit_button:
        # try:
            st.write("Point1:", Point1)
            st.write("Point2:", Point2)
            lat_1, long_1 = Point1.strip('()').split(', ')
            lat_1 = float(lat_1)
            long_1 = float(long_1)
            lat_2, long_2 = Point2.strip('()').split(', ')
            lat_2 = float(lat_2)
            long_2 = float(long_2)
            # st.write(lat_1, long_1)
            # st.write(lat_2, long_2)
            test2(lat_1,long_1,lat_2,long_2)

        # except:
        #     st.write("Invalid input")



        # st.write(type(Point1))

        # G_drive = ox.graph_from_point(Point1, dist=7500, network_type="drive_service") # ดาวน์โหลดเครือข่ายถนนในรัศมีที่ใหญ่ขึ้นเพื่อให้ครอบคลุมทั้งจุดเริ่มต้นและปลายทาง

        # orig_node = ox.distance.nearest_nodes(G_drive, Point1[1], Point1[0])
        # dest_node = ox.distance.nearest_nodes(G_drive, Point2[1], Point2[0])

if __name__ == "__main__":
    test()
