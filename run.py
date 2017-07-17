
def monica(src, maxletters=None):
	tome = {
		97: "yes",
		98: "like this?",
		99: "tell me,",
		100: "teach me,",
		101: "yes",
		102: "shape me,",
		103: "sir",
		104: "as you like,",
		105: "yes",
		106: "this right?",
		107: "like that?",
		108: "go on",
		109: "show me,",
		110: "please sir",
		111: "yes",
		112: "god",
		113: "in here?",
		114: "oh sir",
		115: "so good",
		116: "you like that?",
		117: "yes",
		118: "in there?",
		119: "Jesus",
		120: "that right?",
		121: "god yes,",
		122: "in there?",
		65: "I need it,",
		66: "I know,",
		67: "I want it,",
		68: "Mister",
		69: "I deserve it,",
		70: "I need it,",
		71: "my god",
		72: "I am yours,",
		73: "I need it,",
		74: "I know,",
		75: "I deserve it,",
		76: "Mother",
		77: "teacher",
		78: "I am yours,",
		79: "I want it,",
		80: "I need it,",
		81: "I know,",
		82: "preacher",
		83: "I need it,",
		84: "I deserve it,",
		85: "I want it,",
		86: "I need it,",
		87: "Father",
		88: "my dear",
		89: "I deserve it,",
		90: "senator",
		44: "more sir,",
		45: "go on sir,",
		48: 'lower?',
		49: "more?",
		50: "louder?",
		51: "wider?",
		52: "tighter?",
		54: "looser?",
		55: "wetter?",
		56: "again?",
		57: "faster?",
		58: "slower?",
	}
	her = []
	for c in src[:maxletters]:
		call = tome.get(ord(c))
		if call:
			her.append(call)
	return her

def monica_test():
	print monica("abcde", 2)
	print monica("Badlands")

monica_test()