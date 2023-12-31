import batdongsan_phase1
import batdongsan_phase2
import batdongsan_phase3
import nhatot_phase1
import nhatot_phase2
import nhatot_phase3

if __name__ == "__main__":

    # # Generating list of website links to scrape
    # print("Scraping batdongsan.com.vn: Running Phase 1...")
    # batdongsan_phase1.scrape_links()
    # print("Scraping batdongsan.com.vn: Phase 1 completed.")

    # Scraping websites
    print("Scraping batdongsan.com.vn: Running Phase 2...")
    batdongsan_phase2.scrape_data()
    print("Scraping batdongsan.com.vn: Phase 2 completed.")

    # Refine data (remove duplicates, etc)
    print("Scraping batdongsan.com.vn: Running Phase 3...")
    batdongsan_phase3.remove_duplicates()
    print("Scraping batdongsan.com.vn: Phase 3 completed.")

    # Generating list of website links to scrape
    print("Scraping nhatot.com: Running Phase 1...")
    nhatot_phase1.scrape_links()
    print("Scraping nhatot.com: Phase 1 completed.")

    # Scraping websites
    print("Scraping nhatot.com: Running Phase 2...")
    nhatot_phase2.scrape_data()
    print("Scraping nhatot.com: Phase 2 completed.")

    # Refine data (remove duplicates, etc)
    print("Scraping nhatot.com: Running Phase 3...")
    nhatot_phase3.remove_duplicates()
    print("Scraping nhatot.com: Phase 3 completed.")
