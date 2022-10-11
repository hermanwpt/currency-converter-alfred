import sys
from utils.common_utils import get_query


query = get_query()
sys.stdout.write(query[0] + ";" + query[1])
