from enum import Enum
from .Internal.RepeatedCapability import VALUE_DEFAULT
from .Internal.RepeatedCapability import VALUE_EMPTY


# noinspection SpellCheckingInspection
class Instance(Enum):
	"""Global Repeated capability Instance \n
	Selects the instrument"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Inst1 = 1
	Inst2 = 2
	Inst3 = 3
	Inst4 = 4
	Inst5 = 5
	Inst6 = 6
	Inst7 = 7
	Inst8 = 8
	Inst9 = 9
	Inst10 = 10
	Inst11 = 11
	Inst12 = 12
	Inst13 = 13
	Inst14 = 14
	Inst15 = 15
	Inst16 = 16
	Inst17 = 17
	Inst18 = 18
	Inst19 = 19
	Inst20 = 20
	Inst21 = 21
	Inst22 = 22
	Inst23 = 23
	Inst24 = 24
	Inst25 = 25
	Inst26 = 26
	Inst27 = 27
	Inst28 = 28
	Inst29 = 29
	Inst30 = 30
	Inst31 = 31
	Inst32 = 32


# noinspection SpellCheckingInspection
class Antenna(Enum):
	"""Repeated capability Antenna \n
	Antennas"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8


# noinspection SpellCheckingInspection
class Band(Enum):
	"""Repeated capability Band \n
	Band"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr2 = 2
	Nr5 = 5


# noinspection SpellCheckingInspection
class BandwidthA(Enum):
	"""Repeated capability BandwidthA \n
	Bandwidth"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Bw10 = 10
	Bw20 = 20


# noinspection SpellCheckingInspection
class BandwidthB(Enum):
	"""Repeated capability BandwidthB \n
	Bandwidth"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Bw5 = 5
	Bw10 = 10
	Bw20 = 20


# noinspection SpellCheckingInspection
class BandwidthC(Enum):
	"""Repeated capability BandwidthC \n
	Bandwidth"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Bw5 = 5
	Bw10 = 10
	Bw20 = 20
	Bw40 = 40


# noinspection SpellCheckingInspection
class BandwidthD(Enum):
	"""Repeated capability BandwidthD \n
	Bandwidth"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Bw20 = 20
	Bw40 = 40
	Bw80 = 80
	Bw160 = 160
	Bw8080 = 8080


# noinspection SpellCheckingInspection
class BandwidthE(Enum):
	"""Repeated capability BandwidthE \n
	Bandwidth"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Bw5 = 5
	Bw10 = 10
	Bw20 = 20
	Bw40 = 40
	Bw80 = 80
	Bw160 = 160
	Bw8080 = 8080


# noinspection SpellCheckingInspection
class Channel(Enum):
	"""Repeated capability Channel \n
	content channel index"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2


# noinspection SpellCheckingInspection
class Channels(Enum):
	"""Repeated capability Channels \n
	Selects the Channel"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8


# noinspection SpellCheckingInspection
class Connector(Enum):
	"""Repeated capability Connector \n
	connector"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4


# noinspection SpellCheckingInspection
class Mimo(Enum):
	"""Repeated capability Mimo \n
	Antenna/Stream"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8


# noinspection SpellCheckingInspection
class Reserved(Enum):
	"""Repeated capability Reserved \n
	reserved index"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3


# noinspection SpellCheckingInspection
class ResourceUnit(Enum):
	"""Repeated capability ResourceUnit \n
	Resource Unit"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40
	Nr41 = 41
	Nr42 = 42
	Nr43 = 43
	Nr44 = 44
	Nr45 = 45
	Nr46 = 46
	Nr47 = 47
	Nr48 = 48
	Nr49 = 49
	Nr50 = 50
	Nr51 = 51
	Nr52 = 52
	Nr53 = 53
	Nr54 = 54
	Nr55 = 55
	Nr56 = 56
	Nr57 = 57
	Nr58 = 58
	Nr59 = 59
	Nr60 = 60
	Nr61 = 61
	Nr62 = 62
	Nr63 = 63
	Nr64 = 64
	Nr65 = 65
	Nr66 = 66
	Nr67 = 67
	Nr68 = 68
	Nr69 = 69
	Nr70 = 70
	Nr71 = 71
	Nr72 = 72
	Nr73 = 73
	Nr74 = 74


# noinspection SpellCheckingInspection
class RxAntenna(Enum):
	"""Repeated capability RxAntenna \n
	RxAntenna"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8


# noinspection SpellCheckingInspection
class Segment(Enum):
	"""Repeated capability Segment \n
	selects the segment"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2


# noinspection SpellCheckingInspection
class SegmentB(Enum):
	"""Repeated capability SegmentB \n
	Number of the segment"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32


# noinspection SpellCheckingInspection
class Smi(Enum):
	"""Repeated capability Smi \n
	number"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr4 = 4


# noinspection SpellCheckingInspection
class SMimoPath(Enum):
	"""Repeated capability SMimoPath \n
	selects the count of paths"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Count2 = 2
	Count4 = 4
	Count8 = 8


# noinspection SpellCheckingInspection
class Spatial(Enum):
	"""Repeated capability Spatial \n
	subband index"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4


# noinspection SpellCheckingInspection
class Stream(Enum):
	"""Repeated capability Stream \n
	Stream"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8


# noinspection SpellCheckingInspection
class TrueMimoPath(Enum):
	"""Repeated capability TrueMimoPath \n
	selects the count of paths"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Count1 = 1
	Count2 = 2
	Count3 = 3
	Count4 = 4


# noinspection SpellCheckingInspection
class User(Enum):
	"""Repeated capability User \n
	User"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40
	Nr41 = 41
	Nr42 = 42
	Nr43 = 43
	Nr44 = 44
	Nr45 = 45
	Nr46 = 46
	Nr47 = 47
	Nr48 = 48
	Nr49 = 49
	Nr50 = 50
	Nr51 = 51
	Nr52 = 52
	Nr53 = 53
	Nr54 = 54
	Nr55 = 55
	Nr56 = 56
	Nr57 = 57
	Nr58 = 58
	Nr59 = 59
	Nr60 = 60
	Nr61 = 61
	Nr62 = 62
	Nr63 = 63
	Nr64 = 64
	Nr65 = 65
	Nr66 = 66
	Nr67 = 67
	Nr68 = 68
	Nr69 = 69
	Nr70 = 70
	Nr71 = 71
	Nr72 = 72
	Nr73 = 73
	Nr74 = 74


# noinspection SpellCheckingInspection
class UserIx(Enum):
	"""Repeated capability UserIx \n
	user index"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40
	Nr41 = 41
	Nr42 = 42
	Nr43 = 43
	Nr44 = 44
	Nr45 = 45
	Nr46 = 46
	Nr47 = 47
	Nr48 = 48
	Nr49 = 49
	Nr50 = 50
	Nr51 = 51
	Nr52 = 52
	Nr53 = 53
	Nr54 = 54
	Nr55 = 55
	Nr56 = 56
	Nr57 = 57
	Nr58 = 58
	Nr59 = 59
	Nr60 = 60
	Nr61 = 61
	Nr62 = 62
	Nr63 = 63
	Nr64 = 64
	Nr65 = 65
	Nr66 = 66
	Nr67 = 67
	Nr68 = 68
	Nr69 = 69
	Nr70 = 70
	Nr71 = 71
	Nr72 = 72
	Nr73 = 73
	Nr74 = 74


# noinspection SpellCheckingInspection
class UtError(Enum):
	"""Repeated capability UtError \n
	Antenna/Stream"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
