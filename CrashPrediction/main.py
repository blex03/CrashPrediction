from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import numpy as np
import math


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-form', methods=['POST'])
def submit_form():
    output = request.get_json()
    
    time = output['time']
    date = output['date']
    day = output['day']
    weather = output['weather']
    light = output['light']
    street = output['street']
    city = output['city']
    x = output['latitude']
    y = output['longitude']

    #data code
    city = city.lower()
    cities = {'brookfield': (41.4825947, -73.4095652),
            'guilford': (41.2889866, -72.6817616),
            'stonington': (41.3359327, -71.9059042),
            'suffield': (41.9816944, -72.6506604),
            'new milford': (41.5867418, -73.41176538312553),
            'plainville': (41.6711395, -72.8672429),
            'windham': (41.8208345, -72.0051201),
            'east windsor': (41.9156316, -72.6130726),
            'norwich': (41.5243537, -72.0759008),
            'vernon': (41.8382921, -72.4663331),
            'glastonbury': (41.7123218, -72.608146),
            'cromwell': (41.5949942, -72.6455665),
            'danbury': (41.394817, -73.4540111),
            'bethel': (41.372643, -73.412668),
            'east haven': (41.2762081, -72.8684337),
            'farmington': (41.7198216, -72.8320435),
            'hamden': (41.3959302, -72.8968574),
            'shelton': (41.370196, -73.150955),
            'west hartford': (41.7620447, -72.7420399),
            'westhartford': (41.7608174, -72.73897051387095),
            'north haven': (41.3909305, -72.859545),
            'berlin': (41.621488, -72.7456519),
            'orange': (41.2784304, -73.0256609),
            'enfield': (41.9789387, -72.5755109),
            'groton': (41.3501598, -72.0761998),
            'bristol': (41.6735209, -72.9464859),
            'madison': (41.2794282, -72.5983151),
            'norwalk': (41.1175966, -73.4078968),
            'simsbury': (41.8759152, -72.8012211),
            'avon': (41.8098209, -72.8306541),
            'east hartford': (41.7823216, -72.6120346),
            'granby': (41.9539032, -72.7894272),
            'ridgefield': (41.267211, -73.49345520437956),
            'monroe': (41.3325962, -73.2073358),
            'milford': (41.2222218, -73.0570603),
            'clinton': (41.2756115, -72.52853197757256),
            'old saybrook': (41.2917652, -72.3761956),
            'waterford': (41.358659, -72.1519367),
            'plainfield': (41.6764876, -71.915073),
            'new london': (41.3556187, -72.0997804),
            'newtown': (41.4134764, -73.3086445),
            'wethersfield': (41.7142665, -72.6525922),
            'seymour': (41.3943578, -73.0741697),
            'southington': (41.6005435, -72.8782941),
            'weston': (41.2021302, -73.3812743),
            'windsor locks': (41.9281305, -72.643631),
            'middlebury': (41.5278742, -73.1276107),
            'cheshire': (41.4989861, -72.900658),
            'new canaan': (41.146763, -73.4948446),
            'rocky hill': (41.6648216, -72.6392587),
            'waterbury': (41.5538091, -73.0438362),
            'coventry': (41.7700987, -72.3050803),
            'east hampton': (41.5758442, -72.5024804),
            'easthampton': (42.2903681, -72.6236574),
            'bridgeport': (41.1792695, -73.1887863),
            'new britain': (41.6612104, -72.7795419),
            'south windsor': (41.8489872, -72.5717551),
            'plymouth': (41.6720318, -73.0528893),
            'middletown': (41.5623178, -72.6509061),
            'southbury': (41.4814848, -73.2131693),
            'chaplin': (41.7948205, -72.1272989),
            'goshen': (41.8317624, -73.2251145),
            'north canaan': (42.0225, -73.2908333),
            'ledyard': (41.4386053, -72.0175193),
            'marlborough': (41.631488, -72.459808),
            'essex': (41.3617945, -72.4317473),
            'putnam': (41.9153094, -71.9092563),
            'greenwich': (41.0264862, -73.6284598),
            'windsor': (41.8525984, -72.6437022),
            'thompson': (41.9587089, -71.8625715),
            'east lyme': (41.3569909, -72.2258709),
            'stamford': (41.0534302, -73.5387341),
            'mansfield': (41.7782147, -72.2131565),
            'killingly': (41.8430634, -71.8795925),
            'prospect': (41.5023192, -72.9787163),
            'oxford': (41.4351795, -73.1172769),
            'woodbridge': (41.352597, -73.0084385),
            'harwinton': (41.7712085, -73.05983),
            'durham': (41.473678, -72.68226650231054),
            'new haven': (41.3082138, -72.9250518),
            'north stonington': (41.4411845, -71.8812698),
            'woodbury': (41.5445404, -73.2090025),
            'willington': (41.874428, -72.2598935),
            'east granby': (41.9412081, -72.7273158),
            'tolland': (41.818446, -72.3562252),
            'ashford': (41.8731532, -72.1214653),
            'roxbury': (41.5568282, -73.3088922),
            'hartford': (41.764582, -72.6908547),
            'litchfield': (41.767249, -73.2543049),
            'brooklyn': (41.7881541, -71.9497957),
            'warren': (41.7428733, -73.3487304),
            'manchester': (41.7813345, -72.5304550138903),
            'montville': (41.4649811, -72.1538184),
            'pomfret': (41.8975977, -71.9625736),
            'somers': (41.9853742, -72.4461952),
            'salisbury': (41.983426, -73.4212318),
            'haddam': (41.4773213, -72.5120333),
            'torrington': (41.8006523, -73.1212214),
            'chester': (41.4031547, -72.4509204),
            'colchester': (41.5756543, -72.3320269),
            'preston': (41.5268022, -71.982138),
            'stafford': (41.9851964, -72.2895812),
            'lebanon': (41.6362097, -72.2125789),
            'woodstock': (41.9484307, -71.9739626),
            'new hartford': (41.8823187, -72.9770488),
            'watertown': (41.6062078, -73.1181658),
            'wallingford': (41.4570418, -72.8231552),
            'bethany': (41.4217637, -72.9970496),
            'lisbon': (41.5866851, -72.0207809),
            'trumbull': (41.2428742, -73.2006687),
            'thomaston': (41.6739862, -73.073164),
            'fairfield': (41.1412078, -73.2637258),
            'bolton': (41.7689878, -72.4334173),
            'kent': (41.7246894, -73.476921),
            'morris': (41.6842633, -73.1962245),
            'bethlehem': (41.6393626, -73.2080798),
            'beacon falls': (41.4428745, -73.062608),
            'winchester': (41.918741999999995, -73.10450029832403),
            'sharon': (41.8792599, -73.4767897),
            'barkhamsted': (41.9292629, -72.9139904),
            'washington': (41.6314845, -73.3106731),
            'meriden': (41.5381535, -72.8070435),
            'new fairfield': (41.4664832, -73.4856789),
            'west haven': (41.2706527, -72.9470471),
            'old lyme': (41.3159315, -72.3289715),
            'hebron': (41.6578767, -72.3659161),
            'westport': (41.1414855, -73.3578955),
            'naugatuck': (41.4860186, -73.0509432),
            'middlefield': (41.5165161, -72.7120793),
            'bozrah': (41.5505962, -72.168238),
            'canterbury': (41.6984209, -71.9710811),
            'hampton': (41.7839873, -72.0547977),
            'griswold': (41.6035026, -71.9622443),
            'franklin': (41.6089873, -72.1459112),
            'branford': (41.2795414, -72.8150989),
            'westbrook': (41.285377, -72.4475874),
            'darien': (41.0787079, -73.4692873),
            'union': (41.9909296, -72.1572992),
            'derby': (41.33028, -73.0772546),
            'east haddam': (41.4529215, -72.4613902),
            'cornwall': (41.8437058, -73.3292848),
            'deep river': (41.3856546, -72.4356422),
            'killingworth': (41.3581545, -72.5637023),
            'columbia': (41.7020432, -72.3011917),
            'andover': (41.7373212, -72.37036),
            'sherman': (41.5792607, -73.4956795),
            'stratford': (41.1845415, -73.1331651),
            'ellington': (41.9039863, -72.4698071),
            'salem': (41.491269, -72.2762084),
            'sterling': (41.707599, -71.828682),
            'norfolk': (41.9939828, -73.2020577),
            'burlington': (41.7692648, -72.9645484),
            'newington': (41.6978777, -72.7237063),
            'eastford': (41.902068, -72.0799095),
            'voluntown': (41.5706544, -71.8703497),
            'colebrook': (41.9895388, -73.0956646),
            'north branford': (41.3275971, -72.7673198),
            'scotland': (41.6981999, -72.082083),
            'hartland': (41.996206, -72.9795488),
            'sprague': (41.6214071, -72.0663666),
            'ansonia': (41.3423505, -73.043713),
            'bridgewater': (41.5350949, -73.3662305),
            'canaan': (41.9616667, -73.3083333),
            'redding': (41.3025956, -73.3834532),
            'wolcott': (41.6023196, -72.9867718),
            'portland': (41.5728924, -72.6406905),
            'bloomfield': (41.826488, -72.7300945),
            'canton': (41.8245424, -72.8937122),
            'wilton': (41.1953739, -73.4378988),
            'easton': (41.2528738, -73.2973394),
            'lyme': (41.391095199999995, -72.35110142568081),
            'mashantucket': (41.4644695, -71.9747539)
    }
    weather_domain = [
                        'Snow', 
                        'Freezing Rain or Freezing Drizzle', 
                        'Clear', 
                        'Rain',
                        'Blowing Snow', 
                        'Cloudy', 
                        'Fog, Smog, Smoke', 
                        'Sleet or Hail ',
                        'Other', 
                        'Unknown', 
                        'Severe Crosswinds', 
                        'Not Applicable',
                        'Blowing Sand, Soil, Dirt'
                    ]
    weather_dict = {weather_domain[i]: i+1 for i in range(len(weather_domain))}

    light_domain = ['Dark-Lighted', 'Dark-Not Lighted', 'Daylight', 'Dusk', 'Other',
       'Dawn', 'Unknown', 'Dark-Unknown Lighting']
    light_dict = {light_domain[i]: i+1 for i in range(len(light_domain))}
    
    street_type_dict = {'State': 1, 'Local': 2, 'USRoute': 3, 'Interstate': 4, 'Unknown': 0}

    day = day.lower()
    days = {'sunday' : 1, 
            'monday' : 2,
            'tuesday' : 3,
            'wednesday' : 4,
            'thursday' : 5,
            'friday' : 6,
            'saturday' : 7}
    
    time = time[:2]

    final_centroids = [[ 0.47542116,  0.50484932,  0.07304638, -0.05301978,  0.97249763,
          0.20370676,  0.99703643,  0.06823873,  0.3943536 ,  0.45936926,
          3.42229751,  3.80745381,  2.36393275],
        [ 0.43663976,  0.48714561,  0.04676571, -0.03081628,  0.96972538,
          0.21566179,  0.99691276,  0.07010541,  0.37942323,  0.42014805,
          3.29398822,  1.46642056,  2.42725472],
        [ 0.47281976,  0.53023597,  0.73970211,  0.38114805,  0.97279364,
          0.21140277,  0.9966894 ,  0.07218464,  0.41486601,  0.4579956 ,
          1.14717304,  1.97380373,  2.55064832],
        [ 0.44561182,  0.51060108,  0.33565473,  0.12984376,  0.97378703,
          0.20133846,  0.99690112,  0.07037607,  0.39929692,  0.42954761,
          6.27877203,  1.92455947,  2.56167401]]

    vector = []
    max_y = -71.7879399999999
    min_y = -73.7178249999999

    max_x = 42.04844 
    min_x = 40.9946340000001

    max_city_y = -71.828682
    min_city_y = -73.6284598

    max_city_x = 42.2903681
    min_city_x = 41.0264862

    vector.append((x - min_x) / (max_x - min_x))
    vector.append((y - min_y) / (max_y - min_y))
    vector.append(date_angles(day_of_year(date), "cos"))
    vector.append(date_angles(day_of_year(date), "sin"))
    vector.append(hour_angles(time, "cos"))
    vector.append(hour_angles(time, "sin"))
    vector.append(dotw_angles(days[day], "cos"))
    vector.append(dotw_angles(days[day], "sin"))
    vector.append((cities[city][0] - min_city_x) / (max_city_x - min_city_x))
    vector.append((cities[city][1] - min_city_y) / (max_city_y - min_city_y))
    vector.append(weather_dict[weather])
    vector.append(street_type_dict[street])
    vector.append(light_dict[light])

    print(vector)

    assignment = centroid_selection(vector, final_centroids)


    

    #end
    response_data = {
        'assignment': assignment,
        'message': 'Data received and processed successfully'
    }
    
    # Send the modified data back to JavaScript
    return jsonify(response_data)

def date_angles(date, trig):
    angle = (2*math.pi*date)/365
    if trig == 'cos':
        return np.cos(angle)
    else:
        return np.sin(angle)
    
def day_of_year(date_str):
    try:
        date_object = datetime.strptime(date_str, '%m/%d')
        day_of_year = date_object.timetuple().tm_yday
        return day_of_year
    
    except ValueError:
        return 59
    
def hour_angles(hour, trig):
    hour = int(hour)
    hour += 1
    angle = (2*math.pi*hour)/24
    if trig == 'cos':
        return np.cos(angle)
    else:
        return np.sin(angle)
    
def dotw_angles(dotw, trig):
    angle = (2*math.pi*dotw)/7
    if trig == 'cos':
        return np.cos(angle)
    else:
        return np.sin(angle)
    
def centroid_selection(vector, final_centroids):
    min = float('inf')
    cent_idx = 0
    for cent in range(len(final_centroids)):
        distance = 0
        for i in range(len(vector)):
            distance += (final_centroids[cent][i] - vector[i])**2
        distance = np.sqrt(distance)
        if distance < min:
            cent_idx = cent
            min = distance
    
    return cent_idx
    
if __name__ == "__main__":
    app.run(debug=True)