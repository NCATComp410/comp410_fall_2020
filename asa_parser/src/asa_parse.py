import json
import re
from asa_parser import ShowTech


class AsaParser(ShowTech):
    """Parses an ASA specific show tech"""

    def clock(self):
        """Returns show clock timestamp"""
        return json.dumps({'timestamp': self.get_show_section('clock')})

    def failover_history(self):
        """Returns failover history"""

        # Initialize variables
        fh_list = []    # This will hold the failover info
        timestamp = ''  # Timestamp of the current group information
        group_found = False  # Identifies if parser has found a group

        # --- show failover history ---
        for line in self.get_show_section('failover history'):
            # Check for a timestamp
            if ' UTC ' in line:
                timestamp = line
                group_found = True
            elif group_found:
                data = re.split(r'\s{2,}', line)[1:]
                fh = {'group': data[0],
                      'timestamp': timestamp,
                      'FromState': data[1],
                      'ToState': data[2],
                      'Reason': data[3]}
                fh_list.append(fh)
                group_found = False
        return json.dumps(fh_list)

    def show_process_cpu_hog(self):
        """Parser for process cpu-hog"""
        #return json.dumps({'text': self.get_show_section('process cpu-hog')})
        
        config_errors = []

        last_line = ''

        # parse each line from the show tech section
        # one line at a time
        for line in self.get_show_section('process cpu-hog'):
            
            if line.startswith('Process:'):
                errs = {'Process': line.split('Process:')[1].strip()}
                config_errors.append(errs)
            elif line.startswith('LASTHOG At:'):
                errs = {'Last Hog': line.split('LASTHOG At:')[1].strip()}
                config_errors.append(errs)

            elif line.startswith('PC:'):
                errs = {'PC': line.split('PC:')[1].strip()}
                config_errors.append(errs)

            elif line.startswith('Call stack:'):
                errs = {'Call Stack': line.split('Call stack:')[1].strip()}
                config_errors.append(errs)

            else:
                errs = {'Info': line}
                config_errors.append(errs)
            last_line = line

        return json.dumps(config_errors)

    def startup_config_errors(self):
        """Parser for show startup-config errors"""
        # Create a list which will be a list of dicts
        # which will be returned as a json string
        config_errors = []

        # This will be a holder for the last line parsed
        # Will use this to handle the special case where
        # an ERROR wraps to the next line
        last_line = ''

        # parse each line from the show tech section
        # one line at a time
        for line in self.get_show_section('startup-config errors'):
            # !! MIO module heartbeat failure detected
            if line.startswith('!! '):
                # We'll call a line that starts with !!_ a critical error
                # One way to parse this is to use split() as shown below
                errs = {'CriticalError': line.split('!! ')[1]}

                # line[3:] would also work because it would return
                # line with the first 3 characters removed.
                # errs = {'CriticalError': line[3:]}

                config_errors.append(errs)

            # INFO: Admin context is required to get the interfaces
            elif line.startswith('INFO: '):
                info = {'Info': line.split('INFO: ')[1]}
                config_errors.append(info)

            # *** Output from config line 166, "arp rate-limit 32768"
            elif line.startswith('*** '):
                stars = {'StarInfo': line.split('*** ')[1]}
                config_errors.append(stars)

            # WARNING: No 'anyconnect image' commands have been
            elif line.startswith('WARNING:'):
                warn = {'Warning': line.split('WARNING: ')[1]}
                config_errors.append(warn)

            # ERROR is a little tricker because it's possible the data will
            # wrap to the next line like this:
            #   ERROR: Inspect configuration of this type exists, first remove
            #   that configuration and then add the new configuration
            elif line.startswith('ERROR: '):
                config_errors.append({'Error': line.split('ERROR: ')[1]})

            else:
                # if the last line was ERROR then assume the line wrapped
                if last_line.startswith('ERROR: '):
                    config_errors.append({'Error': line})

            # keep track of the last line parsed so we can handle the
            # ERROR special case
            last_line = line

        return json.dumps(config_errors)

    def show_tech_support_license(self):
        """Parser for show tech support license"""
        #return json structure
        support_license = []

        for line in self.get_show_section('tech-support license'):
            if line.startswith('Registration:'):
                rgs = {'Registration:': line.split('Registration:')[1]}
                support_license.append(rgs)

            if line.startswith('Handle:'):
                info = {'Handle:': line.split('Handle:')[1]}
                support_license.append(info)

            if line.startswith('    License:'):
                license = {'    License:': line.split('    License:')[1]}
                support_license.append(license)

            if line.startswith('    Description:'):
                desc = {'    Description:': line.split('    Description:')[1]}
                support_license.append(desc)

            if line.startswith('    Count:'):
                count = {'    Count:': line.split('    Count:')[1]}
                support_license.append(count)

            if line.startswith('    Version:'):
                vers = {'    Version:': line.split('    Version:')[1]}
                support_license.append(vers)

            if line.startswith('    Status:'):
                stat = {'    Status:': line.split('    Status:')[1]}
                support_license.append(stat)

            if line.startswith('Reservation'):
                res = {'Reservation':line.split('Reservation')[1]}
                support_license.append(res)

        return json.dumps(support_license)

    def show_cpu_usage(self):
        """Parser for show cpu usage"""
        usage = []
        for line in self.get_show_section('cpu usage'):
            if 'CPU ' in line:
                data = line.split(';')
                #print(data)
            usage.append(data)
        return json.dumps(usage)

    def show_memory_region(self):
        """Parser for show_memory region"""
        memory_region = []
        info = ''

        for line in self.get_show_section('memory region'):
            if 'ASLR ' in line:
                info = line
                memory_region.append(info)
            # only parse lines that are not blank
            elif len(line):
                # print(line)
                data = re.split(r'\s+', line)
                mem = {'Address': data[0],
                       'Perm': data[1],
                       'Offset': data[2],
                       'Dev': data[3],
                       'Inode': data[4],
                       'Pathname': data[5]}
                memory_region.append(mem)
        return json.dumps(memory_region)

    def show_cpu_detailed(self):
        """Parser for show cpu detailed"""
        return json.dumps({'text': self.get_show_section('cpu detailed')})

    def ipsec_stats(self):
            """Parser for show ipsec stats"""
            stats = []
            headerinfo = ""
            headerdict = {}
            dict = {}
            for line in self.get_show_section("ipsec stats"):
                if(("Inbound" in line and not ': ' in line)  or ("Outbound" in line and not ': ' in line)):
                    if(headerinfo == "Inbound"):
                        headerinfo = line.strip()
                        stats.append(headerdict)
                        dict = {}
                        headerdict = {headerinfo : dict}

                    else:
                        headerinfo = line.strip()
                        headerdict = {headerinfo : dict}

                elif(re.search("\s{2,}", line)):
                    if ': ' in line:
                      split_line = line.split(": ")
                      dict.update({split_line[0].strip() : split_line[1].strip()})

                else:

                    if (headerinfo == "Outbound"):
                        stats.append(headerdict)
                        headerdict = {}
                        dict = {}
                        headerinfo = ""

                    if ': ' in line:
                        split_line = line.split(": ")
                        stats.append({split_line[0].strip(): split_line[1].strip()})
            return json.dumps(stats)

    def show_memory(self):
        """Parser for show memory"""
        memory = [] #where all the show_memory information will be held
        bucket = {} #holds informtion for one show memory section
        for line in self.get_show_section("memory"):
            if ('Total' in line):
                data = line.split(':')
                bucket[data[0]] = data[1].strip()
                memory.append(bucket)
                bucket = {} #After we get to total reset the dictoary
            else:
                if "%" in line:
                    data = line.split(":")
                    bucket[data[0]] = data[1].strip()
        return json.dumps(memory)

    def show_memory_detail(self):
        memory_detail = []
        get_heap = False
        total = False
        get_mempool = False
        get_fragmented = False
        allocated_memory_stats = False
        for line in self.get_show_section('memory detail'):
            if "Heap" in line:
                get_heap = True

            if get_heap:
                if '-' not in line:
                    data = line.split(':')
                    memory_detail.append({data[0].strip():data[1].strip()})
            elif total:
                data = line.split(':')
                memory_detail.append({data[0].strip():data[1].strip()})
                total = False

            if get_mempool:
                if '---' not in line:
                    data = line.split("=")
                memory_detail.append({data[0].strip():data[1].strip()})

            if get_fragmented or allocated_memory_stats:
                data = re.findall(r'\d+\**', line)
                fragmented = {}
                if data:
                    fragmented['fragment size'] = data[0]
                    fragmented['count'] = data[1]
                    fragmented['total'] = data[2]
                    memory_detail.append(fragmented)

            if "MEMPOOL" in line or 'pool' in line:
                get_mempool = True
                allocated_memory_stats = False

            if line.startswith('----- allocated'):
                allocated_memory_stats = True
                get_fragmented = False
                memory_detail.append(fragmented)

            if line.startswith('----- fragmented'):
                get_fragmented = True

            if '---' in line:
                if get_heap:
                    get_heap = False
                    total = True
                if get_mempool:
                    get_mempool = False
                continue
        return json.dumps(memory_detail)

    def show_tech_support_detail(self):
        """Parser for show cpu detailed"""
        return json.dumps({'text': self.get_show_section('tech-support detail')})

    def show_context_details(self):
        """Parser for show context details"""
        context = []

        #Creating error for context details
        for line in self.get_show_section('context detail'):
            # Context "system", is a system resource
            if line.startswith('Context "system",'):
                sys = {'System': line.split('Context "system",')[1]}
                context.append(sys)

            if line.startswith('Context "admin",'):
                ad = {'Admin': line.split('Context "admin",')[1]}
                context.append(ad)

            if line.startswith('Context "inside1",'):
                in1 = {'Inside1': line.split('Context "inside1",')[1]}
                context.append(in1)

            if line.startswith('Context "inside2",'):
                in2 = {'Inside2': line.split('Context "inside2",')[1]}
                context.append(in2)

            if line.startswith('Context "inside-6-7-9-10",'):
                in6 = {'Inside6': line.split('Context "inside-6-7-9-10",')[1]}
                context.append(in6)

            if line.startswith('Context "inside2-6",'):
                in26 = {'Inside2-6': line.split('Context "inside2-6",')[1]}
                context.append(in26)

            if line.startswith('Context "inside11",'):
                in11 = {'Inside11': line.split('Context "inside11",')[1]}
                context.append(in11)

            if line.startswith('Context "inside13",'):
                in13 = {'Inside13': line.split('Context "inside13",')[1]}
                context.append(in13)

            if line.startswith('Context "inside14",'):
                in14 = {'Inside14': line.split('Context "inside14",')[1]}
                context.append(in14)

            if line.startswith('Context "inside4",'):
                in4 = {'Inside4': line.split('Context "inside4",')[1]}
                context.append(in4)

            if line.startswith('Context "inside2-1",'):
                in21 = {'Inside2-1': line.split('Context "inside2-1",')[1]}
                context.append(in21)

            if line.startswith('Context "inside2-2",'):
                in22 = {'Inside2-2': line.split('Context "inside2-2",')[1]}
                context.append(in22)

            if line.startswith('Context "inside2-4",'):
                in24 = {'Inside2-4': line.split('Context "inside2-4",')[1]}
                context.append(in24)

            if line.startswith('Context "null",'):
                null = {'Null': line.split('Context "null",')[1]}
                context.append(null)

        return json.dumps(context)

    def show_interface(self):
        """Parser for show interface"""
        return json.dumps({'text': self.get_show_section('interface')})

    def show_traffic(self):
        """Parser for show traffic"""
        traffic = {}
        section = ''
        for line in self.get_show_section('traffic'):
            if len(line):  #detects non indented line
                if line == line.lstrip():
                    section = line
                else:
                    if section not in traffic:  #add sub sections
                        traffic[section] = []
                        traffic[section].append(line)
            else:
                if section not in traffic:
                    traffic[section] = {}

                if 'received' in line:
                    direction = 'receive'
                elif 'transmitted' in line:
                    direction = 'transmit'
                else:
                    if direction not in traffic[section]:
                        traffic[section][direction] = []
                    traffic[section][direction].append(line)
        return json.dumps(traffic)

    def show_process(self):
        """Parser for show process"""
        return json.dumps({'text': self.get_show_section('process')})

    def show_logging_buffered(self):
        """Parser for show show logging buffered"""
        logs = {}
        """regex to make sure logged information is in correct format"""
        for line in self.get_show_section('logging buffered'):
            regex = "\w+\s+\d+\s+\d{4}\s+\d+\:+\d+\:+\d+\s+KP-systest-admin\s+\:\s+%ASA-4-711004\:\s+Task ran for \d+\s+\w+\,+\s+Process = \w+\s*\w*\s*\w*\, PC = \w+\, Call stack = "
            logs.append({'text:': re.search(regex, line, flags=0).group(0)})

        return json.dumps(logs)

    def show_kernel_process(self):
        """Parser for show kernel process"""
        return json.dumps({'text': self.get_show_section('kernel process')})
