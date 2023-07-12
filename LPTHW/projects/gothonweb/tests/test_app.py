from app import app

app.config['TESTING'] = True
web = app.test_client()

def test_index():
    rv = web.get('/', follow_redirects=True)
    assert rv.status_code == 200
    assert b"Central Corridor" in rv.data
    
    data = {'action': 'shoot!'}
    rv = web.post('/game', follow_redirects=True, data=data)
    assert b"Quick on the draw you yank" in rv.data
    assert b"Play Again?" in rv.data

def test_successful_run():
    rv = web.get('/', follow_redirects=True)
    
    data = {'action': 'tell a joke'}
    rv = web.post('/game', follow_redirects=True, data=data)
    assert b"Laser Weapon Armory" in rv.data
    
    data = {'action': '0132'}
    rv = web.post('/game', follow_redirects=True, data=data)
    assert b"The Bridge" in rv.data
    
    data = {'action': 'slowly place the bomb'}
    rv = web.post('/game', follow_redirects=True, data=data)
    assert b"Escape Pod" in rv.data
    
    data = {'action': '2'}
    rv = web.post('/game', follow_redirects=True, data=data)
    assert b"You jump into pod 2" in rv.data
    
def test_escape_pod_death():
    rv = web.get('/', follow_redirects=True)
    
    data = {'action': 'tell a joke'}
    rv = web.post('/game', follow_redirects=True, data=data)
    
    data = {'action': '0132'}
    rv = web.post('/game', follow_redirects=True, data=data)
    
    data = {'action': 'slowly place the bomb'}
    rv = web.post('/game', follow_redirects=True, data=data)
    
    data = {'action': '*'}
    rv = web.post('/game', follow_redirects=True, data=data)
    assert b"You jump into a random pod" in rv.data
    assert b"Play Again?" in rv.data
    
def test_bridge_death():
    rv = web.get('/', follow_redirects=True)
    
    data = {'action': 'tell a joke'}
    rv = web.post('/game', follow_redirects=True, data=data)
    
    data = {'action': '0132'}
    rv = web.post('/game', follow_redirects=True, data=data)
    
    data = {'action': 'throw the bomb'}
    rv = web.post('/game', follow_redirects=True, data=data)
    assert b"In a panic you throw the" in rv.data
    assert b"Play Again?" in rv.data
    
def test_armory_death():
    rv = web.get('/', follow_redirects=True)
    
    data = {'action': 'tell a joke'}
    rv = web.post('/game', follow_redirects=True, data=data)
    
    data = {'action': '*'}
    rv = web.post('/game', follow_redirects=True, data=data)
    assert b"The lock buzzes one last time" in rv.data
    assert b"Play Again?" in rv.data
    
def test_armory_death():
    rv = web.get('/', follow_redirects=True)
    
    data = {'action': 'tell a joke'}
    rv = web.post('/game', follow_redirects=True, data=data)
    
    data = {'action': '666'}
    rv = web.post('/game', follow_redirects=True, data=data)
    assert b"The lock buzzes one last time" in rv.data
    assert b"Play Again?" in rv.data
    
def test_corridor_death():
    rv = web.get('/', follow_redirects=True)
    
    data = {'action': 'dodge!'}
    rv = web.post('/game', follow_redirects=True, data=data)
    assert b"Like a world class boxer" in rv.data
    assert b"Play Again?" in rv.data